with open('backup/models/college/faculty.py', 'r') as f:
    lines = f.readlines()
for i, line in enumerate(lines[:35], 1):
    print(f"{i:3}: {repr(line)}")
