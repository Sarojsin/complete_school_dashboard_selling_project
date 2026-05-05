import sqlite3
import re
from collections import defaultdict

# Read script.txt
with open('script.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract SQL code block
sql_match = re.search(r'```(?:\w+)?\s*(.*?)\s*```', content, re.DOTALL)
raw_sql = sql_match.group(1)

# Split into lines for line-by-line processing
lines = raw_sql.split('\n')

# Container for processed statements
processed = []
create_table_stack = []  # stack of (tablename, lines_before_closing_paren)
alter_constraints = defaultdict(list)  # tablename -> list of constraint definitions
in_create = False
current_create_table = None
create_indent = ''
paren_depth = 0
comment_lines = []

def clean_line(line):
    """Remove PostgreSQL-specific syntax and convert types"""
    # Remove comments
    line = re.sub(r'--.*', '', line)
    
    # Data type conversions (before other processing)
    line = re.sub(r'\bBIGSERIAL\b', 'INTEGER', line)
    line = re.sub(r'\bSERIAL\b', 'INTEGER', line)
    line = re.sub(r'\bBIGINT\b', 'INTEGER', line)
    line = re.sub(r'\bINT\b', 'INTEGER', line)
    line = re.sub(r'\bVARCHAR\([^)]*\)\b', 'TEXT', line)
    line = re.sub(r'\bCHAR\([^)]*\)\b', 'TEXT', line)
    line = re.sub(r'\bDECIMAL\([^)]*\)\b', 'REAL', line)
    line = re.sub(r'\bNUMERIC\([^)]*\)\b', 'REAL', line)
    line = re.sub(r'\bTIMESTAMP\b', 'DATETIME', line)
    line = re.sub(r'\bJSONB?\b', 'TEXT', line)
    line = re.sub(r'\bINET\b', 'TEXT', line)
    line = re.sub(r'\bTSVECTOR\b', 'TEXT', line)
    line = re.sub(r'\bBYTEA\b', 'BLOB', line)
    line = re.sub(r'\bUUID\b', 'TEXT', line)
    line = re.sub(r'\bSMALLINT\b', 'INTEGER', line)
    
    # Defaults
    line = line.replace("DEFAULT CURRENT_TIMESTAMP", "DEFAULT (datetime('now'))")
    line = line.replace("DEFAULT CURRENT_DATE", "DEFAULT (date('now'))")
    line = re.sub(r'\bDEFAULT\s+TRUE\b', 'DEFAULT 1', line, flags=re.IGNORECASE)
    line = re.sub(r'\bDEFAULT\s+FALSE\b', 'DEFAULT 0', line, flags=re.IGNORECASE)
    line = re.sub(r"DEFAULT\s+'([^']*)'", r"DEFAULT '\1'", line)
    
    # Remove PostgreSQL-specific clauses
    line = re.sub(r'CREATE\s+EXTENSION\s+IF\s+NOT\s+EXISTS\s+\w+;?', '', line, flags=re.IGNORECASE)
    line = re.sub(r'\s+USING\s+GIN\s*\([^)]*\)', '', line, flags=re.IGNORECASE)
    line = re.sub(r'GENERATED\s+ALWAYS\s+AS\s*\([^)]*\)\s+STORED', '', line, flags=re.IGNORECASE)
    line = re.sub(r'ON\s+UPDATE\s+CURRENT_TIMESTAMP', '', line, flags=re.IGNORECASE)
    
    # Remove partial indexes entirely (they start with CREATE INDEX ... WHERE)
    if 'WHERE' in line and re.search(r'CREATE\s+(UNIQUE\s+)?INDEX', line, re.IGNORECASE):
        return ''  # skip this line
    
    # Remove COLLATE, COMMENT, ENGINE
    line = re.sub(r'\s+COLLATE\s+[^\s,]+', '', line, flags=re.IGNORECASE)
    line = re.sub(r'COMMENT\s*=\s*\'[^\']*\'', '', line, flags=re.IGNORECASE)
    line = re.sub(r'ENGINE\s*=\s*\w+', '', line, flags=re.IGNORECASE)
    line = re.sub(r'DEFAULT\s+CHARSET\s*=\s*\w+', '', line, flags=re.IGNORECASE)
    
    # Remove trailing commas before close parenthesis that might cause syntax errors
    # (handled later)
    
    return line

# First pass: collect ALTER TABLE constraints
i = 0
while i < len(lines):
    line = lines[i]
    
    # Check for ALTER TABLE ADD CONSTRAINT
    alter_match = re.search(r'ALTER\s+TABLE\s+(\w+)\s+ADD\s+CONSTRAINT\s+(\w+)\s+(.*)', line, re.IGNORECASE)
    if alter_match:
        tbl = alter_match.group(1)
        constraint_name = alter_match.group(2)
        constraint_def = alter_match.group(3).rstrip(',')
        alter_constraints[tbl].append(f"  CONSTRAINT {constraint_name} {constraint_def}")
        i += 1
        continue
        
    # Handle multi-line ALTER TABLE (comma separated)
    if line.strip().upper().startswith('ALTER TABLE') and 'ADD CONSTRAINT' in line.upper():
        # Collect continuation lines
        constraint_lines = [line]
        paren_count = line.count('(') - line.count(')')
        j = i + 1
        while j < len(lines) and paren_count > 0:
            constraint_lines.append(lines[j])
            paren_count += lines[j].count('(') - lines[j].count(')')
            j += 1
        # Parse
        full_alter = ' '.join(constraint_lines)
        m = re.search(r'ALTER\s+TABLE\s+(\w+)\s+ADD\s+CONSTRAINT\s+(\w+)\s+(.*)', full_alter, re.IGNORECASE)
        if m:
            tbl = m.group(1)
            constraint_name = m.group(2)
            constraint_def = m.group(3).rstrip(',;')
            # Remove trailing comma; and any ON DELETE CASCADE etc keep
            alter_constraints[tbl].append(f"  CONSTRAINT {constraint_name} {constraint_def}")
        i = j
        continue
    
    i += 1

print(f"Collected constraints for {len(alter_constraints)} tables")

# Second pass: build CREATE TABLE statements with merged constraints
i = 0
while i < len(lines):
    line = lines[i]
    cleaned = clean_line(line)
    if not cleaned.strip():
        i += 1
        continue
        
    # Detect CREATE TABLE
    create_match = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', cleaned, re.IGNORECASE)
    if create_match:
        table_name = create_match.group(1)
        # Start collecting CREATE TABLE
        create_lines = [cleaned]
        # Find the opening parenthesis
        paren_depth = 0
        i += 1
        while i < len(lines):
            next_line = lines[i]
            cleaned_next = clean_line(next_line)
            # Count parentheses
            paren_depth += cleaned_next.count('(') - cleaned_next.count(')')
            create_lines.append(cleaned_next)
            if paren_depth <= 0 and ')' in cleaned_next:
                break
            i += 1
        
        # Insert any ALTER TABLE constraints before closing parenthesis
        if table_name in alter_constraints:
            # Insert before the last line which should be ')'
            for constraint in alter_constraints[table_name]:
                create_lines.insert(-1, constraint)
        
        # Reconstruct statement
        full_create = ' '.join(create_lines)
        # Clean up
        full_create = re.sub(r'\s+', ' ', full_create).strip()
        # Ensure it ends with semicolon
        if not full_create.endswith(';'):
            full_create += ';'
        
        processed.append(full_create)
    
    elif cleaned.upper().startswith('CREATE INDEX') or cleaned.upper().startswith('CREATE UNIQUE INDEX'):
        # Keep index statements (but remove partial ones already filtered)
        processed.append(cleaned)
    
    i += 1

print(f"Generated {len(processed)} statements")

# Save for review
with open('final_schema.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(processed))

# Execute
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
print(f"\nCreated {len(tables)} tables:")
for t in tables:
    print(f"  {t[0]}")

if errors:
    print(f"\nFirst 15 errors:")
    for idx, stmt, err in errors[:15]:
        print(f"  [{idx}] {err}: {stmt[:150]}")
else:
    print("No errors - all tables created successfully!")

conn.close()
