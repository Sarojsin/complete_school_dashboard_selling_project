import sqlite3
import re

def to_sqlite(sql):
    """Convert PostgreSQL DDL to SQLite"""
    result = sql
    
    # Remove comments
    result = re.sub(r'--[^\n]*\n', '\n', result)
    
    # Convert data types
    result = re.sub(r'\bBIGSERIAL\b', 'INTEGER', result)  # We'll add AUTOINCREMENT separately
    result = re.sub(r'\bSERIAL\b', 'INTEGER', result)
    result = re.sub(r'\bBIGINT\b', 'INTEGER', result)
    result = re.sub(r'\bINT\b', 'INTEGER', result)
    result = re.sub(r'\bVARCHAR\([^)]*\)\b', 'TEXT', result)
    result = re.sub(r'\bCHAR\([^)]*\)\b', 'TEXT', result)
    result = re.sub(r'\bDECIMAL\([^)]*\)\b', 'REAL', result)
    result = re.sub(r'\bNUMERIC\([^)]*\)\b', 'REAL', result)
    result = re.sub(r'\bTIMESTAMP\b', 'DATETIME', result)
    result = re.sub(r'\bJSONB?\b', 'TEXT', result)
    result = re.sub(r'\bINET\b', 'TEXT', result)
    
    # Handle AUTOINCREMENT correctly: only for columns named "id"
    result = re.sub(r'id\s+INTEGER\s+PRIMARY\s+KEY\s+AUTOINCREMENT\s+PRIMARY\s+KEY', 
                    'id INTEGER PRIMARY KEY AUTOINCREMENT', result)
    result = re.sub(r'id\s+INTEGER\s+PRIMARY\s+KEY\s+AUTOINCREMENT', 
                    'id INTEGER PRIMARY KEY AUTOINCREMENT', result)
    result = re.sub(r'id\s+INTEGER\s+PRIMARY\s+KEY', 
                    'id INTEGER PRIMARY KEY AUTOINCREMENT', result)
    
    # Fix default values
    result = result.replace("DEFAULT CURRENT_TIMESTAMP", "DEFAULT (datetime('now'))")
    result = result.replace("DEFAULT CURRENT_DATE", "DEFAULT (date('now'))")
    result = re.sub(r'DEFAULT\s+TRUE', 'DEFAULT 1', result, flags=re.IGNORECASE)
    result = re.sub(r'DEFAULT\s+FALSE', 'DEFAULT 0', result, flags=re.IGNORECASE)
    # Preserve string defaults
    result = re.sub(r"DEFAULT\s+'([^']*)'", r"DEFAULT '\1'", result)
    
    # Remove PostgreSQL-specific syntax
    result = re.sub(r'CREATE\s+EXTENSION\s+IF\s+NOT\s+EXISTS\s+\w+;?', '', result, flags=re.IGNORECASE)
    result = re.sub(r'CREATE\s+INDEX\s+[^(]*USING\s+GIN\s*\([^)]*\);?', '', result, flags=re.IGNORECASE)
    result = re.sub(r'GENERATED\s+ALWAYS\s+AS\s*\([^)]*\)\s+STORED', '', result, flags=re.IGNORECASE)
    result = re.sub(r'ON\s+UPDATE\s+CURRENT_TIMESTAMP', '', result, flags=re.IGNORECASE)
    
    # Fix partial indexes - remove WHERE clause
    result = re.sub(r'CREATE\s+(UNIQUE\s+)?INDEX\s+[^(]*\([^)]*\)\s+WHERE\s+[^;]+;?', 
                    lambda m: '' if 'WHERE' in m.group(0) else m.group(0), result, flags=re.IGNORECASE)
    
    # Remove COLLATE and COMMENT clauses
    result = re.sub(r'COLLATE\s+[^\s,]+', '', result, flags=re.IGNORECASE)
    result = re.sub(r'COMMENT\s*=\s*\'[^\']*\'', '', result, flags=re.IGNORECASE)
    result = re.sub(r'ENGINE\s*=\s*\w+', '', result, flags=re.IGNORECASE)
    result = re.sub(r'DEFAULT\s+CHARSET\s*=\s*\w+', '', result, flags=re.IGNORECASE)
    
    # Fix CHECK constraints - keep them as is
    # Already handled, but ensure proper syntax
    
    # Fix ALTER TABLE constraints to use proper SQLite syntax
    result = re.sub(r'ADD\s+CONSTRAINT\s+fk_', 'ADD CONSTRAINT fk_', result)
    
    # Clean up extra commas and spaces
    result = re.sub(r',\s*\n\s*\)', '\n)', result)
    result = re.sub(r'[\n\r]+', ' ', result)
    result = re.sub(r'\s+', ' ', result)
    result = result.replace(' ;', ';')
    
    # Split on semicolons while preserving them
    statements = []
    parts = result.split(';')
    for part in parts:
        part = part.strip()
        if part:
            statements.append(part + ';')
    
    return statements

# Read script.txt
with open('script.txt', 'r', encoding='utf-8') as f:
    content = f.read()

sql_match = re.search(r'```(?:\w+)?\s*(.*?)\s*```', content, re.DOTALL)
if not sql_match:
    print("ERROR: No SQL found")
    exit(1)

raw_sql = sql_match.group(1)

# Convert
statements = to_sqlite(raw_sql)
print(f"Converted {len(statements)} statements")

# Save for debugging
with open('debug_sqlite.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(statements))

# Create fresh database
import os
if os.path.exists('school_sell.db'):
    os.remove('school_sell.db')
    print("Removed existing database")

conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

created = 0
errors = []

for i, stmt in enumerate(statements, 1):
    try:
        cursor.execute(stmt)
        created += 1
    except sqlite3.OperationalError as e:
        errors.append((i, stmt[:200], str(e)))
    except sqlite3.IntegrityError as e:
        errors.append((i, stmt[:200], str(e)))

conn.commit()

# Verify
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print(f"\nCreated {len(tables)} tables")
for t in tables:
    print(f"  {t[0]}")

if errors:
    print(f"\nErrors ({len(errors)}):")
    for idx, stmt, err in errors[:20]:
        print(f"  [{idx}] {err}: {stmt}")

conn.close()
