# School Notes Exceptions
# ======================

class NoteException(Exception):
    """Base exception for notes module"""
    pass


class NoteNotFoundException(NoteException):
    """Note not found exception"""
    def __init__(self, note_id: int):
        self.note_id = note_id
        super().__init__(f"Note with ID {note_id} not found")


class InvalidFileTypeException(NoteException):
    """Invalid file type exception"""
    def __init__(self, file_type: str):
        self.file_type = file_type
        super().__init__(f"Invalid file type: {file_type}")


class FileTooLargeException(NoteException):
    """File too large exception"""
    def __init__(self, size: int, max_size: int):
        self.size = size
        self.max_size = max_size
        super().__init__(f"File size {size} exceeds maximum {max_size} bytes")


class NoteAccessDeniedException(NoteException):
    """Access denied exception"""
    def __init__(self, note_id: int, user_id: int):
        self.note_id = note_id
        self.user_id = user_id
        super().__init__(f"User {user_id} cannot access note {note_id}")


class FileUploadException(NoteException):
    """File upload exception"""
    def __init__(self, message: str):
        super().__init__(f"File upload failed: {message}")


class InvalidFileExtensionException(NoteException):
    """Invalid file extension exception"""
    def __init__(self, extension: str):
        self.extension = extension
        super().__init__(f"Invalid file extension: {extension}")


__all__ = [
    "NoteException",
    "NoteNotFoundException",
    "InvalidFileTypeException",
    "FileTooLargeException",
    "NoteAccessDeniedException",
    "FileUploadException",
    "InvalidFileExtensionException"
]