with open('modules/school/school_assignments/models.py', 'r') as f:
    lines = f.readlines()
for i, line in enumerate(lines[24:29], start=25):
    print(f"{i}: {repr(line)}")
