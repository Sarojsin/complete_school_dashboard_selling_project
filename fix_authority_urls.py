import re
import os

# Define the replacements
replacements = {
    "url_for('authority.dashboard')": "url_for('authority_dashboard')",
    "url_for('authority.students')": "url_for('authority_students')",
    "url_for('authority.teachers')": "url_for('authority_teachers')",
    "url_for('authority.courses')": "url_for('authority_courses')",
    "url_for('authority.fees')": "url_for('authority_fees')",
    "url_for('authority.notices')": "url_for('authority_notices')",
    "url_for('authority.add_notice')": "url_for('authority_add_notice')",
    "url_for('authority.edit_notice',": "url_for('authority_edit_notice',",
    "url_for('authority.delete_notice',": "url_for('authority_delete_notice',",
    "url_for('authority.delete_course',": "url_for('authority_delete_course',",
    "url_for('authority.delete_student',": "url_for('authority_delete_student',",
    "url_for('authority.delete_teacher',": "url_for('authority_delete_teacher',",
}

# Files to update
files = [
    r"c:\Users\U S E R\OneDrive\Desktop\claud\templates\authority\add_notice.html",
    r"c:\Users\U S E R\OneDrive\Desktop\claud\templates\authority\edit_course.html",
    r"c:\Users\U S E R\OneDrive\Desktop\claud\templates\authority\edit_notice.html",
    r"c:\Users\U S E R\OneDrive\Desktop\claud\templates\authority\edit_student.html",
    r"c:\Users\U S E R\OneDrive\Desktop\claud\templates\authority\edit_teacher.html",
    r"c:\Users\U S E R\OneDrive\Desktop\claud\templates\authority\notices.html",
    r"c:\Users\U S E R\OneDrive\Desktop\claud\templates\authority\add_teacher.html",
    r"c:\Users\U S E R\OneDrive\Desktop\claud\templates\authority\add_fee.html",
    r"c:\Users\U S E R\OneDrive\Desktop\claud\templates\authority\add_course.html",
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply all replacements
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated: {file_path}")
    else:
        print(f"File not found: {file_path}")

print("All files updated successfully!")
