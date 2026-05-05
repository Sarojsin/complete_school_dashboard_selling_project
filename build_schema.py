import sqlite3
import re
from collections import defaultdict

# -------------------------------------------------------------
# STEP 1: Read and extract SQL from script.txt
# -------------------------------------------------------------
with open('script.txt', 'r', encoding='utf-8') as f:
    content = f.read()

sql_match = re.search(r'```(?:\w+)?\s*(.*?)\s*```', content, re.DOTALL)
raw_sql = sql_match.group(1)

lines = raw_sql.split('\n')
print(f"Total lines in raw SQL: {len(lines)}")

# -------------------------------------------------------------
# STEP 2: First pass - collect ALTER TABLE ADD CONSTRAINT statements
# -------------------------------------------------------------
alter_constraints = defaultdict(list)  # table_name -> list of constraint definitions
i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.upper().startswith('ALTER TABLE') and 'ADD CONSTRAINT' in line.upper():
        # Gather the full ALTER TABLE statement across multiple lines
        stmt_parts = []
        paren_depth = 0
        while i < len(lines):
            l = lines[i]
            stmt_parts.append(l)
            paren_depth += l.count('(') - l.count(')')
            if ';' in l and paren_depth <= 0:
                break
            i += 1
        full_stmt = ' '.join(stmt_parts)
        # Parse: ALTER TABLE table_name ADD CONSTRAINT constraint_name definition;
        m = re.search(r'ALTER\s+TABLE\s+(\w+)\s+ADD\s+CONSTRAINT\s+(\w+)\s+(.*?);', full_stmt, re.IGNORECASE)
        if m:
            tbl, cname, cdef = m.group(1), m.group(2), m.group(3).rstrip(', ')
            alter_constraints[tbl].append(f"  CONSTRAINT {cname} {cdef}")
        i += 1
        continue
    i += 1

print(f"Collected constraints for {len(alter_constraints)} tables")

# -------------------------------------------------------------
# STEP 3: Second pass - parse CREATE TABLE and merge constraints
# -------------------------------------------------------------
i = 0
processed = []   # final SQLite statements list
in_create = False
current_table = None
create_header = None
body_lines = []
paren_depth = 0

def convert_types_and_defaults(text):
    """Apply PostgreSQL->SQLite conversions to a chunk of SQL"""
    # Data types
    text = re.sub(r'\bBIGSERIAL\b', 'INTEGER', text, flags=re.IGNORECASE)
    text = re.sub(r'\bSERIAL\b', 'INTEGER', text, flags=re.IGNORECASE)
    text = re.sub(r'\bBIGINT\b', 'INTEGER', text, flags=re.IGNORECASE)
    text = re.sub(r'\bINT\b', 'INTEGER', text, flags=re.IGNORECASE)
    text = re.sub(r'\bVARCHAR\([^)]*\)\b', 'TEXT', text, flags=re.IGNORECASE)
    text = re.sub(r'\bCHAR\([^)]*\)\b', 'TEXT', text, flags=re.IGNORECASE)
    text = re.sub(r'\bDECIMAL\([^)]*\)\b', 'REAL', text, flags=re.IGNORECASE)
    text = re.sub(r'\bNUMERIC\([^)]*\)\b', 'REAL', text, flags=re.IGNORECASE)
    text = re.sub(r'\bTIMESTAMP\b', 'DATETIME', text, flags=re.IGNORECASE)
    text = re.sub(r'\bJSONB?\b', 'TEXT', text, flags=re.IGNORECASE)
    text = re.sub(r'\bINET\b', 'TEXT', text, flags=re.IGNORECASE)
    text = re.sub(r'\bTSVECTOR\b', 'TEXT', text, flags=re.IGNORECASE)
    text = re.sub(r'\bBYTEA\b', 'BLOB', text, flags=re.IGNORECASE)
    text = re.sub(r'\bUUID\b', 'TEXT', text, flags=re.IGNORECASE)
    text = re.sub(r'\bSMALLINT\b', 'INTEGER', text, flags=re.IGNORECASE)
    text = re.sub(r'\bTINYINT\b', 'INTEGER', text, flags=re.IGNORECASE)
    
    # Defaults
    text = text.replace("DEFAULT CURRENT_TIMESTAMP", "DEFAULT (datetime('now'))")
    text = text.replace("DEFAULT CURRENT_DATE", "DEFAULT (date('now'))")
    text = re.sub(r'\bDEFAULT\s+TRUE\b', 'DEFAULT 1', text, flags=re.IGNORECASE)
    text = re.sub(r'\bDEFAULT\s+FALSE\b', 'DEFAULT 0', text, flags=re.IGNORECASE)
    text = re.sub(r"DEFAULT\s+'([^']*)'", r"DEFAULT '\1'", text)
    
    # Remove PostgreSQL-specific
    text = re.sub(r'CREATE\s+EXTENSION\s+IF\s+NOT\s+EXISTS\s+\w+;?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+USING\s+GIN\s*\([^)]*\)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'GENERATED\s+ALWAYS\s+AS\s*\([^)]*\)\s+STORED', '', text, flags=re.IGNORECASE)
    text = re.sub(r'ON\s+UPDATE\s+CURRENT_TIMESTAMP', '', text, flags=re.IGNORECASE)
    text = re.sub(r'COLLATE\s+[^\s,]+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'COMMENT\s*=\s*\'[^\']*\'', '', text, flags=re.IGNORECASE)
    text = re.sub(r'ENGINE\s*=\s*\w+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'DEFAULT\s+CHARSET\s*=\s*\w+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'UNSIGNED', '', text, flags=re.IGNORECASE)
    
    # Remove partial indexes (WHERE clauses)
    text = re.sub(r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+[^(]*\([^)]*\)\s+WHERE\s+[^;]+;?', '', text, flags=re.IGNORECASE)
    
    # Fix multi-constraint ALTER TABLE inline additions: but we'll handle differently
    
    return text

while i < len(lines):
    line = lines[i]
    
    # Detect start of CREATE TABLE
    if not in_create and re.search(r'^CREATE\s+TABLE', line.strip(), re.IGNORECASE):
        in_create = True
        paren_depth = 0
        # Capture header up to '('
        header_match = re.search(r'(CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?\w+\s*)\(', line, re.IGNORECASE)
        if header_match:
            create_header = header_match.group(1).strip() + '('
            # Everything after the first '(' in this line is part of body
            after_paren = line[header_match.end()-1:]  # includes '('
            body_lines = [after_paren]
            paren_depth = after_paren.count('(') - after_paren.count(')')
        else:
            # Shouldn't happen, but fallback
            create_header = line.strip()
            body_lines = [line]
            paren_depth = line.count('(') - line.count(')')
        i += 1
        continue
    
    if in_create:
        # Accumulate lines until we close the outer parenthesis with a semicolon
        clean_line_for_paren = line
        # Exclude comment-only lines from paren counting? Keep them
        paren_depth += clean_line_for_paren.count('(') - clean_line_for_paren.count(')')
        body_lines.append(clean_line_for_paren)
        
        if paren_depth <= 0 and ';' in line:
            # End of CREATE TABLE
            in_create = False
            
            # Build the full body text
            body_text = ' '.join(body_lines)
            # Remove the trailing ';' and closing ')' from last line? Actually body should include )
            # The body includes the final ')' char and maybe ';'
            
            # Convert types within body
            body_converted = convert_types_and_defaults(body_text)
            
            # Inject any ALTER TABLE constraints before final ')'
            # Find table name from header
            tbl_match = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', create_header, re.IGNORECASE)
            if tbl_match:
                tbl_name = tbl_match.group(1)
                if tbl_name in alter_constraints:
                    # Insert constraints before the closing ')'
                    for constraint in alter_constraints[tbl_name]:
                        body_converted = body_converted.rstrip('\n;) ')
                        # Remove trailing characters that might be ')', add comma
                        if not body_converted.endswith(','):
                            body_converted += ','
                        body_converted += f"\n  {constraint}," # trailing comma may cause issue, handle later
            
            # Ensure the statement ends with proper closing
            body_converted = body_converted.rstrip(', \t\n')
            if not body_converted.endswith(')'):
                # find last ')'
                pos = body_converted.rfind(')')
                if pos != -1:
                    body_converted = body_converted[:pos+1]
            if not body_converted.endswith(';'):
                body_converted += ';'
            
            # Clean up any double commas or trailing commas before ')'
            body_converted = re.sub(r',\s*\)', ')', body_converted)
            # Also fix: ,; -> ;
            body_converted = re.sub(r',\s*;', ';', body_converted)
            
            full_statement = create_header + '\n' + body_converted
            # Actually create_header already ends with '(', body_converted should start with content without '('? Wait.
            # In our approach, body_lines includes '(' on first element. So body_converted starts with '(' and ends with ');'
            # So we just need to prepend the header without adding extra '('.
            # Let's reconstruct properly:
            
            # The body_converted currently is the full content inside including parentheses? Let's rebuild.
            # Actually original strategy: create_header ends with '(' so we need to put body content (columns...) then close with ');'.
            # But we have body_lines that started with the '(' included. We applied conversion to entire body_lines including that '('.
            # So we should just use body_converted as the rest after header? Let's simplify: combine header and body_converted.
            
            # Let's reconstruct properly:
            # create_header = "CREATE TABLE name ("
            # body_content = everything from after '(' up to and including closing ');'
            # We derived body_converted from join(body_lines). That string includes the ')' and ';'? In original, body_lines included final ')' and ';'.
            # After conversion, body_converted should still end with ')', then we added semicolon maybe.
            # So final statement should be create_header + body_converted (without duplicating '(').
            # But create_header already has '(' so body_converted must start after '('.
            # Since our first body line included '(' as part of line, we need to strip leading '('.
            
            first_line = body_lines[0]
            # Actually we need to figure out representation.
            
            # Better: Instead of trying to be fancy, let's reassemble:
            # Extract body without the leading '(' from body_converted? Actually create_header ends with '('; body_converted should NOT have that '('.
            # So we need to drop the '(' from body_converted if it starts with '('.
            body_for_sql = body_converted
            if body_for_sql.startswith('('):
                body_for_sql = body_for_sql[1:].lstrip()
            
            full_statement = f"{create_header} {body_for_sql}".strip()
            # Ensure ends with semicolon
            if not full_statement.endswith(';'):
                full_statement += ';'
            
            processed.append(full_statement)
            i += 1
            continue
        else:
            i += 1
            continue
    
    # Skip ALTER TABLE statements (already merged)
    if line.strip().upper().startswith('ALTER TABLE'):
        i += 1
        continue
    
    # Keep other statements: CREATE INDEX, CREATE UNIQUE INDEX, etc.
    # Skip comments
    if line.strip().startswith('--') or not line.strip():
        i += 1
        continue
    
    # It's likely an index statement
    # Convert it lightly
    cleaned = convert_types_and_defaults(line)
    if cleaned.strip():
        processed.append(cleaned)
    
    i += 1

print(f"Generated {len(processed)} statements")

# Save final SQL
with open('final_schema.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(processed))

# -------------------------------------------------------------
# STEP 4: Execute
# -------------------------------------------------------------
import os
if os.path.exists('school_sell.db'):
    os.remove('school_sell.db')

conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

created = 0
errors = []

for idx, stmt in enumerate(processed, 1):
    stmt_clean = stmt.strip()
    if not stmt_clean or stmt_clean.startswith('--'):
        continue
    try:
        cursor.execute(stmt_clean)
        created += 1
    except (sqlite3.OperationalError, sqlite3.IntegrityError) as e:
        errors.append((idx, stmt_clean[:200], str(e)))

conn.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print(f"\nCreated {len(tables)} tables")
for t in tables:
    print(f"  {t[0]}")

if errors:
    print(f"\nErrors ({len(errors)}):")
    for idx, stmt, err in errors[:15]:
        print(f"  [{idx}] {err}")
        print(f"       {stmt[:150]}")
else:
    print("All tables created successfully!")

conn.close()
