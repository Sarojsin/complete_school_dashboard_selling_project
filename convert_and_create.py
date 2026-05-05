import sqlite3
import re

def postgresql_to_sqlite(sql):
    """Convert PostgreSQL DDL to SQLite-compatible SQL"""
    
    conversions = [
        # Data types
        (r'\bBIGSERIAL\b', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
        (r'\bSERIAL\b', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
        (r'\bBIGINT\b', 'INTEGER'),
        (r'\bINT\b', 'INTEGER'),
        (r'\bBOOLEAN\b', 'BOOLEAN'),
        (r'\bTEXT\b', 'TEXT'),
        (r'\bVARCHAR\((\d+)\)\b', r'TEXT'),  # Convert all VARCHAR to TEXT for simplicity
        (r'\bCHAR\((\d+)\)\b', r'TEXT'),
        (r'\bDECIMAL\([^)]+\)\b', r'REAL'),  # All decimals to REAL
        (r'\bNUMERIC\([^)]+\)\b', r'REAL'),
        (r'\bTIMESTAMP\b', r'DATETIME'),
        (r'\bDATE\b', r'DATE'),
        (r'\bTIME\b', r'TIME'),
        (r'\bJSONB\b', r'TEXT'),
        (r'\bJSON\b', r'TEXT'),
        (r'\bINET\b', r'TEXT'),
        (r'\bBYTEA\b', r'BLOB'),
        (r'\bUUID\b', r'TEXT'),
        (r'\bTSVECTOR\b', r'TEXT'),
        
        # Default values
        (r'DEFAULT CURRENT_TIMESTAMP', r"DEFAULT (datetime('now'))"),
        (r'DEFAULT CURRENT_DATE', r"DEFAULT (date('now'))"),
        (r'DEFAULT TRUE', r'DEFAULT 1'),
        (r'DEFAULT FALSE', r'DEFAULT 0'),
        
        # Remove PostgreSQL-specific features
        (r'CREATE EXTENSION IF NOT EXISTS pg_trgm;', r''),
        (r'CREATE INDEX .* USING GIN \([^)]+\);', r''),
        (r'GENERATED ALWAYS AS \([^)]+\) STORED', r''),  # Remove generated columns for now
        (r'ON UPDATE CURRENT_TIMESTAMP', r''),  # SQLite handles this differently
        (r'ON DELETE RESTRICT', r'ON DELETE NO ACTION'),
        (r'CHECK \(([^)]+)\)', lambda m: f"CHECK({m.group(1)})"),  # Simplify checks
        (r'::\w+', r''),  # Remove type casts
        
        # Fix ENUM checks
        (r"CHECK \(user_type IN \('[^']+'(?:,\s*'[^']+')*\)\)", 
         r"CHECK (user_type IN ('student','teacher','parent','admin','staff','librarian','accountant','driver','vendor','alumni'))"),
        (r"CHECK \(assignment_type IN \('[^']+'(?:,\s*'[^']+')*\)\)",
         r"CHECK (assignment_type IN ('homework','project','lab','quiz','essay','other'))"),
        # ... more ENUM patterns could be added
    ]
    
    result = sql
    for pattern, replacement in conversions:
        if callable(replacement):
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        else:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    # Additional cleanups
    result = re.sub(r',\s*\n\s*\)', '\n)', result)  # Remove trailing commas before closing paren
    result = re.sub(r'\s+', ' ', result)  # Normalize whitespace
    result = re.sub(r';\s*', ';\n', result)  # Ensure each statement ends with newline
    
    return result

# Read script.txt
with open('script.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract SQL code block
sql_match = re.search(r'```(?:\w+)?\s*(.*?)\s*```', content, re.DOTALL)
if not sql_match:
    print("ERROR: No SQL code block found")
    exit(1)

raw_sql = sql_match.group(1)

# Convert to SQLite
sqlite_sql = postgresql_to_sqlite(raw_sql)

# Save converted SQL for inspection
with open('converted_schema.sql', 'w', encoding='utf-8') as f:
    f.write(sqlite_sql)

print("Conversion complete. Saved to converted_schema.sql")
print(f"SQL length: {len(sqlite_sql)} characters")

# Split into individual statements
statements = []
lines = sqlite_sql.split('\n')
current = []
depth = 0
in_string = False
string_char = None

for line in lines:
    stripped = line.strip()
    if not stripped or stripped.startswith('--'):
        continue
    
    # Track string literals to avoid splitting inside them
    for char in line:
        if char in ("'", '"') and not in_string:
            in_string = True
            string_char = char
        elif char == string_char and in_string:
            in_string = False
            string_char = None
    
    depth += line.count('(') - line.count(')')
    current.append(line)
    
    if depth == 0 and not in_string and stripped.endswith(';'):
        stmt = ' '.join(current).strip()
        if stmt:
            statements.append(stmt)
        current = []

if current:
    stmt = ' '.join(current).strip()
    if stmt:
        statements.append(stmt)

print(f"Extracted {len(statements)} SQL statements")

# Execute against SQLite
conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

created = 0
errors = []

for i, stmt in enumerate(statements, 1):
    if not stmt.strip():
        continue
    try:
        cursor.execute(stmt)
        created += 1
        if created % 10 == 0:
            print(f"Progress: {created} tables created...")
    except sqlite3.OperationalError as e:
        errors.append((i, stmt[:150], str(e)))

conn.commit()

# Verify
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print(f"\n✓ Successfully created {len(tables)} tables out of {len(statements)} statements")
for table in tables:
    print(f"  - {table[0]}")

if errors:
    print(f"\n✗ Errors ({len(errors)}):")
    for idx, stmt, err in errors[:15]:
        print(f"  [{idx}] {stmt}...: {err}")

conn.close()
