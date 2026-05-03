# School Library Exceptions
# =====================

class LibraryException(Exception):
    """Base exception for library operations"""
    pass


class BookNotFoundException(LibraryException):
    """Book not found exception"""
    def __init__(self, book_id: int):
        self.book_id = book_id
        super().__init__(f"Book with ID {book_id} not found")


class BookNotAvailableException(LibraryException):
    """Book not available exception"""
    def __init__(self, book_id: int):
        self.book_id = book_id
        super().__init__(f"Book with ID {book_id} is not available")


class LoanNotFoundException(LibraryException):
    """Loan not found exception"""
    def __init__(self, loan_id: int):
        self.loan_id = loan_id
        super().__init__(f"Loan with ID {loan_id} not found")


class MaxBooksExceededException(LibraryException):
    """Maximum books exceeded exception"""
    def __init__(self, max_books: int):
        self.max_books = max_books
        super().__init__(f"Maximum number of books ({max_books}) exceeded")


class OverdueBookException(LibraryException):
    """Overdue book exception"""
    def __init__(self, loan_id: int, days_overdue: int):
        self.loan_id = loan_id
        self.days_overdue = days_overdue
        super().__init__(f"Book is overdue by {days_overdue} days")


class InvalidISBNException(LibraryException):
    """Invalid ISBN exception"""
    def __init__(self, isbn: str):
        self.isbn = isbn
        super().__init__(f"Invalid ISBN: {isbn}")


__all__ = [
    "LibraryException",
    "BookNotFoundException",
    "BookNotAvailableException",
    "LoanNotFoundException",
    "MaxBooksExceededException",
    "OverdueBookException",
    "InvalidISBNException"
]