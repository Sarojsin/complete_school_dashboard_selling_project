with open('modules/school/school_notes/models.py', 'r') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if i >= 20 and i <= 30:
        spaces = len(line) - len(line.lstrip(' '))
        print(f"Line {i}: {spaces} spaces | {repr(line[:40])}")
