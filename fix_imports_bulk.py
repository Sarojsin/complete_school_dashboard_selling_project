import os
import re

import sys

def fix_imports(target_dir):
    replacements = [
        (re.compile(r'from models\b'), 'from app.models'),
        (re.compile(r'from services\b'), 'from app.services'),
        (re.compile(r'from repositories\b'), 'from app.repositories'),
        (re.compile(r'from utils\b'), 'from app.utils'),
        (re.compile(r'import utils\b'), 'import app.utils'),
        (re.compile(r'from dependencies\b'), 'from app.dependencies.auth'),
        (re.compile(r'from tables.tables\b'), 'from app.schemas.misc'),
        (re.compile(r'from tables\b'), 'from app.schemas'),
    ]

    for root, dirs, files in os.walk(target_dir):
        # Skip some dirs
        if '__pycache__' in dirs: dirs.remove('__pycache__')
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    try:
                        with open(file_path, 'r', encoding='latin-1') as f:
                            content = f.read()
                    except Exception as e:
                        print(f"Skipping {file_path} due to error: {e}")
                        continue
                
                new_content = content
                for pattern, replacement in replacements:
                    new_content = pattern.sub(replacement, new_content)
                
                if new_content != content:
                    print(f"Fixed imports in: {file_path}")
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    fix_imports(target)
