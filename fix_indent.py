content = open('backup/models/college/faculty.py', 'r').readlines()
# Fix lines 30-34 to use 4 spaces
for i in [30,31,32,33,34]:
    if i-1 < len(content):
        line = content[i-1]
        # Replace leading 5 spaces with 4
        if line.startswith('     '):
            content[i-1] = line[1:]  # remove one leading space
with open('backup/models/college/faculty.py', 'w') as f:
    f.writelines(content)
print("Fixed indentation")
