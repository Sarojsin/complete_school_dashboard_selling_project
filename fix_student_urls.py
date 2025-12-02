import os

replacements = {
    "url_for('student.assignments')": "url_for('student_assignments')",
    "url_for('student.test_list')": "url_for('student_test_list')",
}

files = [
    r"c:\Users\U S E R\OneDrive\Desktop\claud\templates\student\assignments_detail.html",
    r"c:\Users\U S E R\OneDrive\Desktop\claud\templates\student\test_result.html",
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated: {file_path}")

print("Student templates updated!")
