## best_structure.py
import os

# ─────────────────────────────────────
# Ignore junk folders & files
# ─────────────────────────────────────
IGNORE_DIRS = {
    '.git', '.venv', '__pycache__', '.pytest_cache',
    '.idea', '.vscode', 'node_modules',
    'site-packages', 'venv', 'env', '.next', 'dist', 'build'
}

IGNORE_FILES = {
    '.DS_Store', 'tree.txt', 'your_structure.txt', 'server.log'
}

# ─────────────────────────────────────
# Folder name → emoji
# ─────────────────────────────────────
FOLDER_EMOJI = {
    # Backend
    'app': '📱',
    'api': '🔌',
    'core': '🎯',
    'services': '🧠',
    'routes': '🔀',
    'controllers': '🎮',
    'models': '🗄️',
    'schemas': '📐',
    'repositories': '💼',
    'middleware': '🔐',
    'utils': '🔧',
    'helpers': '🛠️',
    'config': '⚙️',
    'database': '🗂️',
    'migrations': '🗃️',

    # Frontend / React
    'frontend': '🖥️',
    'react': '⚛️',
    'src': '📦',
    'components': '🧩',
    'pages': '📄',
    'hooks': '🪝',
    'context': '🌐',
    'store': '🗃️',
    'redux': '🧠',
    'slices': '🍕',
    'assets': '🖼️',
    'public': '🌍',
    'styles': '🎨',

    # Others
    'static': '📁',
    'templates': '🎨',
    'tests': '🧪',
    'scripts': '📜',
    'docs': '📚',
    'media': '🖼️',
    'logs': '📜',
}

# ─────────────────────────────────────
# File extension / name → emoji
# ─────────────────────────────────────
FILE_EMOJI = {
    # Backend code
    '.py': '🐍',
    '.java': '☕',
    '.cpp': '💠',
    '.c': '🔵',
    '.go': '🐹',
    '.rs': '🦀',
    '.php': '🐘',

    # Frontend / React
    '.js': '🟨',
    '.jsx': '⚛️',
    '.ts': '🟦',
    '.tsx': '⚛️',
    '.vue': '🟩',
    '.svelte': '🧡',

    # Web
    '.html': '🌐',
    '.css': '🎨',
    '.scss': '🎨',
    '.sass': '🎨',
    '.less': '🎨',

    # Data
    '.json': '🧾',
    '.yaml': '🧾',
    '.yml': '🧾',
    '.xml': '📄',
    '.csv': '📊',

    # Docs
    '.md': '📝',
    '.txt': '📄',
    '.pdf': '📕',
    '.docx': '📘',

    # Config / Env
    '.env': '🔐',
    '.ini': '⚙️',
    '.cfg': '⚙️',

    # Images
    '.png': '🖼️',
    '.jpg': '🖼️',
    '.jpeg': '🖼️',
    '.svg': '🖌️',
    '.gif': '🎞️',

    # Media
    '.mp4': '🎬',
    '.mp3': '🎵',
    '.wav': '🎵',

    # Archives
    '.zip': '📦',
    '.rar': '📦',
    '.7z': '📦',

    # Database
    '.db': '🗄️',
    '.sqlite3': '🗄️',

    # Logs
    '.log': '📜',
}

# ─────────────────────────────────────
# Emoji resolvers
# ─────────────────────────────────────
def folder_emoji(name):
    return FOLDER_EMOJI.get(name.lower(), '📂')

def file_emoji(filename):
    # Smart filename detection
    if filename in {'package.json'}:
        return '📦'
    if filename.endswith('.lock'):
        return '🔒'
    if filename in {'vite.config.js', 'vite.config.ts'}:
        return '⚡'
    if filename in {'next.config.js'}:
        return '➡️'
    if filename in {'App.jsx', 'App.tsx'}:
        return '⚛️'
    if filename in {'main.jsx', 'main.tsx', 'index.jsx', 'index.tsx'}:
        return '🚀'

    _, ext = os.path.splitext(filename.lower())
    return FILE_EMOJI.get(ext, '📄')

# ─────────────────────────────────────
# Tree printer
# ─────────────────────────────────────
def print_tree(path, prefix='', out=None):
    try:
        items = os.listdir(path)
    except PermissionError:
        return

    items = [
        i for i in items
        if i not in IGNORE_DIRS
        and i not in IGNORE_FILES
        and not i.endswith('.pyc')
    ]

    items.sort()
    dirs = [i for i in items if os.path.isdir(os.path.join(path, i))]
    files = [i for i in items if os.path.isfile(os.path.join(path, i))]
    entries = dirs + files

    for index, item in enumerate(entries):
        full_path = os.path.join(path, item)
        is_last = index == len(entries) - 1
        connector = '└── ' if is_last else '├── '

        if os.path.isdir(full_path):
            icon = folder_emoji(item)
            line = f"{prefix}{connector}{icon} {item}/"
        else:
            icon = file_emoji(item)
            line = f"{prefix}{connector}{icon} {item}"

        out.write(line + '\n')

        if os.path.isdir(full_path):
            extension = '    ' if is_last else '│   '
            print_tree(full_path, prefix + extension, out)

# ─────────────────────────────────────
# Entry point
# ─────────────────────────────────────
if __name__ == "__main__":
    with open('project_detail_emplimenting_plan.md', 'w', encoding='utf-8') as f:
        f.write("school_management_system/\n")
        print_tree('.', '', f)
