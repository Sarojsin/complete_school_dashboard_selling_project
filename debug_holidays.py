import re

with open('script.txt', 'r') as f:
    content = f.read()

sql_match = re.search(r'```(?:\w+)?\s*(.*?)\s*```', content, re.DOTALL)
raw_sql = sql_match.group(1)

statements = [s.strip() for s in re.split(r';\s*\n', raw_sql) if s.strip()]

tbl = 'school_holidays'
print(f"Looking for ALTER TABLE for {tbl}:")
for s in statements:
    s_nc = re.sub(r'--.*', '', s).strip()
    if s_nc.upper().startswith('ALTER TABLE') and f'ALTER TABLE {tbl}' in s_nc:
        print("MATCHED:")
        print(s_nc)
        print()
        parts = re.split(r'ADD\s+CONSTRAINT\s+', s_nc, flags=re.IGNORECASE)
        print(f"Split into {len(parts)} parts")
        for i, part in enumerate(parts):
            print(f"  Part {i}: {part[:100]}")
        break
