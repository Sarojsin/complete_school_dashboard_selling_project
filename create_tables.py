import sqlite3
import re

# Read the SQL from script.txt
with open('script.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract SQL code block
sql_match = re.search(r'```\s*(.*?)\s*```', content, re.DOTALL)
if not sql_match:
    print("ERROR: Could not find SQL code block")
    exit(1)

sql = sql_match.group(1)

# PostgreSQL to SQLite conversions
conversions = [
    # Data types
    (r'BIGSERIAL', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
    (r'BIGINT', 'INTEGER'),
    (r'SERIAL', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
    (r'BOOLEAN', 'BOOLEAN'),
    (r'BOOLEAN DEFAULT TRUE', 'BOOLEAN DEFAULT 1'),
    (r'BOOLEAN DEFAULT FALSE', 'BOOLEAN DEFAULT 0'),
    (r'IS TRUE', '= 1'),
    (r'IS FALSE', '= 0'),
    (r'DECIMAL\(\s*(\d+)\s*,\s*(\d+)\s*\)', r'REAL'),  # Simplify decimals
    (r'TIMESTAMP', 'DATETIME'),
    (r'JSONB', 'TEXT'),
    (r'INET', 'TEXT'),
    (r'BYTEA', 'BLOB'),
    
    # Indexes
    (r'CREATE EXTENSION IF NOT EXISTS pg_trgm;', ''),
    (r'CREATE INDEX .* USING GIN \(to_tsvector\([^)]+\)\);', ''),  # Remove full-text search indexes
    
    # Unique constraints
    (r'CREATE UNIQUE INDEX uk_', 'CREATE UNIQUE INDEX idx_uk_'),
    (r'CREATE UNIQUE INDEX (\w+)_', 'CREATE UNIQUE INDEX idx_\\1_'),
    
    # Default values
    (r'DEFAULT CURRENT_TIMESTAMP', 'DEFAULT (datetime(\'now\'))'),
    (r'DEFAULT CURRENT_DATE', 'DEFAULT (date(\'now\'))'),
    
    # Check constraints - adjust syntax
    (r'CHECK\s*\(([^)]+)\)', lambda m: f"CHECK({m.group(1).replace('>=', '>=').replace('<=', '<=')})"),
    
    # Foreign key syntax stays mostly the same
    # ALTER TABLE ... ADD CONSTRAINT stays the same
    
    # Remove unnecessary clauses
    (r'\s+WHERE deleted_at IS NULL', ''),
    (r'\s+WHERE expiry_date IS NOT NULL', ''),
    (r'\s+WHERE user_id IS NOT NULL', ''),
    (r'\s+WHERE transaction_id IS NOT NULL', ''),
    (r'\s+WHERE isbn IS NOT NULL', ''),
    (r'\s+WHERE student_id IS NOT NULL', ''),
    (r'\s+WHERE teacher_id IS NOT NULL', ''),
    (r'\s+WHERE alumni_id IS NOT NULL', ''),
    (r'\s+WHERE parent_id IS NOT NULL', ''),
    (r'\s+WHERE asset_id IS NOT NULL', ''),
    (r'\s+WHERE appointment_id IS NOT NULL', ''),
]

def replace_multiple(text, replacements):
    result = text
    for pattern, replacement in replacements:
        if callable(replacement):
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        else:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result

# Apply conversions
sqlite_sql = replace_multiple(sql, conversions)

# Additional SQLite-specific adjustments
sqlite_sql = re.sub(r',\s*\n\s*\)', '\n)', sqlite_sql)  # Clean up trailing commas
sqlite_sql = sqlite_sql.replace('pg_trgm', '')  # Remove any remaining extension references

# Split into individual statements
 statements = []
 current = []
 in_multiline_comment = False
 in_string = False
 string_char = None
 paren_depth = 0

for line in sqlite_sql.split('\n'):
    stripped = line.strip()
    
    # Handle comments
    if '/*' in line and '*/' not in line:
        in_multiline_comment = True
        continue
    if '*/' in line:
        in_multiline_comment = False
        continue
    if in_multiline_comment:
        continue
    if stripped.startswith('--'):
        continue
    
    # Track parentheses for statement boundaries
    paren_depth += line.count('(') - line.count(')')
    
    current.append(line)
    
    if paren_depth == 0 and stripped.endswith(';'):
        statements.append(' '.join(current).strip())
        current = []

if current:
    statements.append(' '.join(current).strip())

print(f"Total statements: {len(statements)}")

# Execute against SQLite database
conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

created = 0
errors = []

for i, stmt in enumerate(statements, 1):
    stmt = stmt.rstrip(';')
    if not stmt or stmt.isspace():
        continue
    try:
        cursor.execute(stmt)
        created += 1
        if created % 10 == 0:
            print(f"Created {created} tables...")
    except sqlite3.OperationalError as e:
        errors.append((i, stmt[:100], str(e)))

conn.commit()

# Verify
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print(f"\nSuccessfully created {len(tables)} tables:")
for table in tables:
    print(f"  - {table[0]}")

if errors:
    print(f"\nErrors ({len(errors)}):")
    for idx, stmt, err in errors[:10]:
        print(f"  [{idx}] {stmt}: {err}")

conn.close()
