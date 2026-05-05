import sqlite3
import re
from collections import OrderedDict

# -------------------------------------------------------------
# Load SQL from script.txt
# -------------------------------------------------------------
with open('script.txt', 'r', encoding='utf-8') as f:
    content = f.read()
sql_match = re.search(r'```(?:\w+)?\s*(.*?)\s*```', content, re.DOTALL)
raw_sql = sql_match.group(1)

# -------------------------------------------------------------
# Split into individual statements (respecting that each ends with ;)
# -------------------------------------------------------------
lines = raw_sql.split('\n')
raw_statements = []
buffer = []
for line in lines:
    # Remove line comments to avoid confusion; keep rest
    line_nc = re.sub(r'--.*', '', line)
    buffer.append(line_nc)
    if ';' in line_nc:
        stmt = ' '.join(buffer).strip()
        if stmt:
            raw_statements.append(stmt)
        buffer = []
if buffer:
    stmt = ' '.join(buffer).strip()
    if stmt:
        raw_statements.append(stmt)

print(f"Raw statements: {len(raw_statements)}")

# -------------------------------------------------------------
# Phase 1: Categorize statements
# -------------------------------------------------------------
create_table_stmts = OrderedDict()   # table_name -> original CREATE TABLE stmt (string)
alter_constraints = {}               # table_name -> list of constraint strings
other_statements = []                # other DDL (CREATE INDEX etc)

# Initialize alter_constraints dict for all potential tables
for stmt in raw_statements:
    stmt_upper = stmt.upper()
    if stmt_upper.startswith('ALTER TABLE') and 'ADD CONSTRAINT' in stmt_upper:
        m = re.search(r'ALTER\s+TABLE\s+(\w+)\s+ADD\s+CONSTRAINT\s+(\w+)\s+(.*)', stmt, re.IGNORECASE)
        if m:
            tbl, cname, cdef = m.group(1), m.group(2), m.group(3).rstrip(', ')
            if tbl not in alter_constraints:
                alter_constraints[tbl] = []
            alter_constraints[tbl].append(f"  CONSTRAINT {cname} {cdef}")
    elif stmt_upper.startswith('CREATE TABLE'):
        m = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', stmt, re.IGNORECASE)
        if m:
            tbl = m.group(1)
            create_table_stmts[tbl] = stmt
    elif stmt_upper.startswith('CREATE INDEX') or stmt_upper.startswith('CREATE UNIQUE INDEX'):
        other_statements.append(stmt)
    # else: ignore comments or other

print(f"Found {len(create_table_stmts)} CREATE TABLEs")
print(f"Found ALTER constraints for {len(alter_constraints)} tables")

# -------------------------------------------------------------
# Conversion function
# -------------------------------------------------------------
def convert_sql(text):
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
    # Defaults
    text = text.replace("DEFAULT CURRENT_TIMESTAMP", "DEFAULT (datetime('now'))")
    text = text.replace("DEFAULT CURRENT_DATE", "DEFAULT (date('now'))")
    text = re.sub(r'\bDEFAULT\s+TRUE\b', 'DEFAULT 1', text, flags=re.IGNORECASE)
    text = re.sub(r'\bDEFAULT\s+FALSE\b', 'DEFAULT 0', text, flags=re.IGNORECASE)
    text = re.sub(r"DEFAULT\s+'([^']*)'", r"DEFAULT '\1'", text)
    # Remove PG specifics
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

def find_matching_paren(s, start):
    depth = 0
    for i in range(start, len(s)):
        if s[i] == '(':
            depth += 1
        elif s[i] == ')':
            depth -= 1
            if depth == 0:
                return i
    return -1

# -------------------------------------------------------------
# Phase 2: Build final statements
# -------------------------------------------------------------
final_statements = []

for tbl, create_stmt in create_table_stmts.items():
    # Convert the statement
    converted = convert_sql(create_stmt)
    
    # Find first '('
    try:
        start = converted.index('(')
    except ValueError:
        # fallback: keep as is
        final_statements.append(converted + ';')
        continue
    
    close = find_matching_paren(converted, start)
    if close == -1:
        final_statements.append(converted + ';')
        continue
    
    header = converted[:start].strip()
    body = converted[start+1:close].strip()
    
    # Append constraints if any
    if tbl in alter_constraints:
        for constraint in alter_constraints[tbl]:
            body = body.rstrip()
            if body.endswith(','):
                body += f"\n{constraint},"
            else:
                body += f",\n{constraint},"
    
    # Remove any trailing comma before closing
    body = re.sub(r',\s*$', '', body)
    
    new_stmt = f"{header} (\n{body}\n);"
    final_statements.append(new_stmt)

# Add other statements (indexes)
for stmt in other_statements:
    conv = convert_sql(stmt)
    if not conv.endswith(';'):
        conv += ';'
    final_statements.append(conv)

print(f"Final statement count: {len(final_statements)}")

# -------------------------------------------------------------
# Write to file
# -------------------------------------------------------------
with open('final_schema.sql', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(final_statements))

# -------------------------------------------------------------
# Execute
# -------------------------------------------------------------
import os
if os.path.exists('school_sell.db'):
    os.remove('school_sell.db')
conn = sqlite3.connect('school_sell.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

created = 0
errors = []
for idx, stmt in enumerate(final_statements, 1):
    try:
        cursor.execute(stmt)
        created += 1
    except (sqlite3.OperationalError, sqlite3.IntegrityError, sqlite3.ProgrammingError) as e:
        errors.append((idx, stmt[:200], str(e)))

conn.commit()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()
print(f"\nCreated {len(tables)} tables")
for t in tables:
    print(f"  {t[0]}")
if errors:
    print(f"\nFirst 15 errors:")
    for idx, s, err in errors[:15]:
        print(f"  [{idx}] {err}")
        print(f"       {s[:150]}")
else:
    print("SUCCESS: All tables created without errors!")
conn.close()
