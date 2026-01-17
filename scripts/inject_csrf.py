import os
import re

def inject_csrf_to_templates(directory):
    csrf_input = '\n    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">'
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Find all <form> tags that don't already have CSRF token
                if "<form" in content and 'name="csrf_token"' not in content:
                    # Very simple regex to find form tags and inject after them
                    new_content = re.sub(r'(<form[^>]*>)', r'\1' + csrf_input, content)
                    
                    if content != new_content:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"Injected CSRF into {path}")

if __name__ == "__main__":
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    inject_csrf_to_templates(templates_dir)
