import os

def generate_tree(startpath, exclude_dirs=None, exclude_files=None):
    if exclude_dirs is None:
        exclude_dirs = {'.git', '__pycache__', '.venv', '.pytest_cache', 'node_modules', 'logs', '.gemini', 'tmp'}
    if exclude_files is None:
        exclude_files = {'.DS_Store'}
    
    tree_lines = []
    
    for root, dirs, files in os.walk(startpath):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        dirs.sort()
        files.sort()
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        
        if level == 0:
            tree_lines.append(f"{os.path.basename(startpath)}/")
        else:
            tree_lines.append(f"{'│   ' * (level - 1)}├── {os.path.basename(root)}/")
        
        subindent = '│   ' * (level) + '├── '
        last_subindent = '│   ' * (level) + '└── '
        
        for i, f in enumerate(files):
            if f in exclude_files:
                 continue
            if i == len(files) - 1 and not dirs: # Last file and no subdirs
                 # This logic is a bit simple, strictly making it tree-like is hard with os.walk
                 # Let's stick to the README format provided which uses ├── for everything roughly
                 pass

            tree_lines.append(f"{'│   ' * level}├── {f}")
            
    return "\n".join(tree_lines)

# Better implementation for exact tree structure
def print_tree(directory, prefix=''):
    ignore_dirs = {'.git', '__pycache__', '.venv', '.pytest_cache', 'node_modules', 'logs', '.gemini', 'tmp', 'venv', 'site-packages'}
    ignore_files = {'.DS_Store', '*.pyc'}
    
    files = []
    dirs = []
    
    try:
        entries = sorted(os.listdir(directory))
    except PermissionError:
        return ""

    for entry in entries:
        if entry in ignore_dirs:
            continue
        if entry.startswith('__'):
             continue 
            
        full_path = os.path.join(directory, entry)
        if os.path.isdir(full_path):
            dirs.append(entry)
        else:
            files.append(entry)
            
    entries = files + dirs # Print files then dirs? No usually dirs then files or mix.
    # The user example shows mix. Let's just sort alphabetically.
    all_entries = sorted(files + dirs)
    
    output = ""
    for i, entry in enumerate(all_entries):
        is_last = (i == len(all_entries) - 1)
        
        connector = "└── " if is_last else "├── "
        
        output += f"{prefix}{connector}{entry}\n"
        
        full_path = os.path.join(directory, entry)
        if os.path.isdir(full_path):
            extension = "    " if is_last else "│   "
            output += print_tree(full_path, prefix=prefix + extension)
            
    return output

if __name__ == "__main__":
    current_dir = os.getcwd()
    with open("project_structure.txt", "w", encoding="utf-8") as f:
        f.write("claud/\n")
        f.write(print_tree(current_dir))
    print("Tree generated in project_structure.txt")
