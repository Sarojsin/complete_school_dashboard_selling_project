# School Notes Utils
# =================

import os
import hashlib
from typing import Optional
from datetime import datetime
from .constants import (
    ALLOWED_ALL_EXTENSIONS,
    MAX_FILE_SIZE,
    MAX_VIDEO_SIZE,
    NOTE_TYPE_PDF,
    NOTE_TYPE_VIDEO
)


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return os.path.splitext(filename)[1].lower()


def is_valid_file_extension(filename: str) -> bool:
    """Check if file extension is allowed"""
    ext = get_file_extension(filename)
    return ext in ALLOWED_ALL_EXTENSIONS


def get_file_size_limit(file_type: str) -> int:
    """Get file size limit based on type"""
    if file_type == NOTE_TYPE_VIDEO:
        return MAX_VIDEO_SIZE
    return MAX_FILE_SIZE


def generate_file_name(original_filename: str, teacher_id: int) -> str:
    """Generate unique file name"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ext = get_file_extension(original_filename)
    return f"{teacher_id}_{timestamp}{ext}"


def calculate_file_hash(file_path: str) -> str:
    """Calculate file hash for verification using SHA256"""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def format_file_size(size_bytes: int) -> str:
    """Format file size for display"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def get_file_type_from_extension(extension: str) -> str:
    """Get note type from file extension"""
    ext = extension.lower()
    if ext in ['.pdf']:
        return NOTE_TYPE_PDF
    elif ext in ['.mp4', '.avi', '.mov', '.mkv']:
        return NOTE_TYPE_VIDEO
    # Add more types as needed
    return "document"


def is_valid_file_size(size: int, file_type: str) -> bool:
    """Check if file size is within limit"""
    limit = get_file_size_limit(file_type)
    return size <= limit


__all__ = [
    "get_file_extension",
    "is_valid_file_extension",
    "get_file_size_limit",
    "generate_file_name",
    "calculate_file_hash",
    "format_file_size",
    "get_file_type_from_extension",
    "is_valid_file_size"
]