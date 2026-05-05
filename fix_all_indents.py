import os
files_to_fix = [
    'modules/school/school_assignments/models.py',
    'modules/school/school_notes/models.py',
    'modules/school/school_videos/models.py',
]
for filepath in files_to_fix:
    with open(filepath, 'r') as f:
        lines = f.readlines()
    fixed_lines = []
    for line in lines:
        # If line starts with 5 spaces followed by non-space, reduce to 4
        if line.startswith('     ') and not line.startswith('    ') and line[4] != ' ':
            # Count leading spaces
            spaces = len(line) - len(line.lstrip(' '))
            if spaces > 4:
                line = ' ' * (spaces - 1) + line.lstrip(' ')
        fixed_lines.append(line)
    with open(filepath, 'w') as f:
        f.writelines(fixed_lines)
    print(f"Fixed {filepath}")
