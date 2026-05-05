with open('modules/school/school_notes/models.py', 'r') as f:
    lines = f.readlines()
for i in [23,24,25]:
    line = lines[i-1]
    spaces = len(line) - len(line.lstrip(' '))
    print(f"Line {i}: {spaces} spaces | {repr(line)}")
