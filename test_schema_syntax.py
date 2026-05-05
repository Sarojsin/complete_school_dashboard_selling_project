import subprocess
import sys

# Test syntax by trying to parse each statement with psql's -f but stop on errors, gather count
result = subprocess.run(
    ['psql', 'postgresql://user:tara@localhost:5432/school_sell_db', '-f', 'school_schema_ordered.sql', '-v', 'ON_ERROR_STOP=1'],
    capture_output=True, text=True
)

if result.returncode == 0:
    print("All statements parsed and executed successfully")
else:
    err = result.stderr
    # Count error lines
    error_lines = [l for l in err.split('\n') if 'ERROR' in l or 'syntax error' in l]
    print(f"Errors: {len(error_lines)} found")
    # Show first few
    for l in error_lines[:10]:
        print(l)
    # Also show near context?
    # Let's find line number in error: like "line 2240:"
    import re
    lines = re.findall(r'ERROR:\s*(\d+):', err)
    if lines:
        print("\nError line numbers:", lines)
        # Show those lines from the file
        for line_num in lines[:5]:
            try:
                n = int(line_num)
                with open('school_schema_ordered.sql') as f:
                    lines_all = f.readlines()
                start = max(0, n-3)
                end = min(len(lines_all), n+2)
                print(f"\nAround line {n}:")
                for i in range(start, end):
                    mark = '>>>' if i+1 == n else '   '
                    print(f"{mark} {i+1:5d}: {lines_all[i].rstrip()}")
            except:
                pass
        # Show those lines from the file
        for line_num in lines[:5]:
            try:
                n = int(line_num)
                with open('school_schema_ordered.sql') as f:
                    lines_all = f.readlines()
                start = max(0, n-3)
                end = min(len(lines_all), n+2)
                print(f"\nAround line {n}:")
                for i in range(start, end):
                    mark = '>>>' if i+1 == n else '   '
                    print(f"{mark} {i+1:5d}: {lines_all[i].rstrip()}")
            except:
                pass
