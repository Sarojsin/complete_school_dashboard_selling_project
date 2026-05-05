import sqlite3
import re
from collections import defaultdict

# Read raw SQL from script.txt
with open('script.txt', 'r', encoding='utf-8') as f:
    content = f.read()
sql_match = re.search(r'```(?:\w+)?\s*(.*?)\s*```', content, re.DOTALL)
raw_sql = sql_match.group(1)
lines = raw_sql.split('\n')
print(f"Total input lines: {len(lines)}")

# -------------------------------------------------------------
# Phase 1: Collect ALTER TABLE constraints and mark lines to skip
# -------------------------------------------------------------
alter_constraints = defaultdict(list)  # table_name -> list of constraint definitions
skip_lines = set()  # line indices to skip

i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.upper().startswith('ALTER TABLE'):
        # Find the full statement ending with semicolon
        start_i = i
        stmt_lines = []
        paren_depth = 0
        while i < len(lines):
            l = lines[i]
            stmt_lines.append(l)
            paren_depth += l.count('(') - l.count(')')
            skip_lines.add(i)
            if ';' in l and paren_depth <= 0:
                break
            i += 1
        full_stmt = ' '.join(stmt_lines)
        # Extract table name and constraint definition
        m = re.search(r'ALTER\s+TABLE\s+(\w+)\s+ADD\s+CONSTRAINT\s+(\w+)\s+(.*?);', full_stmt, re.IGNORECASE)
        if m:
            tbl, cname, cdef = m.group(1), m.group(2), m.group(3).rstrip(', ')
            alter_constraints[tbl].append(f"  CONSTRAINT {cname} {cdef}")
        i += 1
        continue
    i += 1

print(f"Found ALTER constraints for {len(alter_constraints)} tables, skipping {len(skip_lines)} lines")

# -------------------------------------------------------------
# Phase 2: Convert and build statements
# -------------------------------------------------------------
def convert_sql_chunk(text):
    """Apply PostgreSQL->SQLite conversions to SQL text"""
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
    # Defaults
    text = text.replace("DEFAULT CURRENT_TIMESTAMP", "DEFAULT (datetime('now'))")
    text = text.replace("DEFAULT CURRENT_DATE", "DEFAULT (date('now'))")
    text = re.sub(r'\bDEFAULT\s+TRUE\b', 'DEFAULT 1', text, flags=re.IGNORECASE)
    text = re.sub(r'\bDEFAULT\s+FALSE\b', 'DEFAULT 0', text, flags=re.IGNORECASE)
    text = re.sub(r"DEFAULT\s+'([^']*)'", r"DEFAULT '\1'", text)
    # Remove PostgreSQL features
    text = re.sub(r'CREATE\s+EXTENSION\s+IF\s+NOT\s+EXISTS\s+\w+;?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+USING\s+GIN\s*\([^)]*\)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'GENERATED\s+ALWAYS\s+AS\s*\([^)]*\)\s+STORED', '', text, flags=re.IGNORECASE)
    text = re.sub(r'ON\s+UPDATE\s+CURRENT_TIMESTAMP', '', text, flags=re.IGNORECASE)
    text = re.sub(r'COLLATE\s+[^\s,]+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'COMMENT\s*=\s*\'[^\']*\'', '', text, flags=re.IGNORECASE)
    text = re.sub(r'ENGINE\s*=\s*\w+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'DEFAULT\s+CHARSET\s*=\s*\w+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'UNSIGNED', '', text, flags=re.IGNORECASE)
    # Remove partial indexes
    text = re.sub(r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+[^(]*\([^)]*\)\s+WHERE\s+[^;]+;?', '', text, flags=re.IGNORECASE)
    return text

processed = []
i = 0
in_create = False
create_header = ''
body_lines = []
paren_depth = 0

while i < len(lines):
    # Skip lines marked from phase 1
    if i in skip_lines:
        i += 1
        continue
    
    line = lines[i]
    stripped = line.strip()
    
    # Start CREATE TABLE
    if not in_create and re.search(r'^CREATE\s+TABLE', stripped, re.IGNORECASE):
        in_create = True
        # Separate header and opening paren
        m = re.search(r'(CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?\w+)', stripped, re.IGNORECASE)
        if m:
            create_header = m.group(1).strip()
            # Everything after the match in the line might include '('
            remainder = stripped[m.end():].strip()
            if remainder.startswith('('):
                # opening paren on same line
                body_lines = [remainder]  # includes '('
                paren_depth = remainder.count('(') - remainder.count(')')
            else:
                body_lines = []
                paren_depth = 0
        else:
            create_header = stripped
            body_lines = []
            paren_depth = 0
        i += 1
        continue
    
    if in_create:
        # Accumulate this line into body
        body_lines.append(line)
        paren_depth += line.count('(') - line.count(')')
        
        # Check if we've closed the CREATE TABLE
        if paren_depth <= 0 and ';' in line:
            # End of CREATE TABLE
            in_create = False
            
            # Build body string
            body_text = ' '.join(body_lines)
            body_converted = convert_sql_chunk(body_text)
            
            # Inject collected constraints for this table before closing ')'
            tbl_match = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', create_header, re.IGNORECASE)
            if tbl_match:
                tbl_name = tbl_match.group(1)
                if tbl_name in alter_constraints:
                    # Insert constraints before ')'
                    for constraint in alter_constraints[tbl_name]:
                        # Ensure body_converted ends without ')'
                        body_converted = body_converted.rstrip()
                        # Remove trailing ')', add constraint with comma
                        if body_converted.endswith(')'):
                            body_converted = body_converted[:-1].rstrip()
                        if not body_converted.endswith(','):
                            body_converted += ','
                        body_converted += f'\n  {constraint},'
            
            # Clean up trailing comma before ')'
            body_converted = re.sub(r',\s*\)', ')', body_converted)
            
            # Reconstruct full statement
            # create_header doesn't include '('; body_converted may start with '('?
            # Our body includes '(' at start from first line.
            # We'll just combine: header + space + body_converted
            full_stmt = f"{create_header} {body_converted}".strip()
            if not full_stmt.endswith(';'):
                full_stmt += ';'
            processed.append(full_stmt)
        i += 1
        continue
    
    # If line is just comment or empty, skip
    if not stripped or stripped.startswith('--'):
        i += 1
        continue
    
    # Anything else (mostly CREATE INDEX statements) - convert and add
    converted = convert_sql_chunk(stripped)
    if converted.strip():
        processed.append(converted)
    
    i += 1

print(f"Total processed statements: {len(processed)}")

# -------------------------------------------------------------
# Phase 3: Write and execute
# -------------------------------------------------------------
with open('final_schema.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(processed))

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
    print(f"\nFirst 20 errors:")
    for idx, stmt, err in errors[:20]:
        print(f"  [{idx}] {err}")
        print(f"       {stmt[:150]}")
else:
    print("SUCCESS: All tables created with no errors!")

conn.close()
