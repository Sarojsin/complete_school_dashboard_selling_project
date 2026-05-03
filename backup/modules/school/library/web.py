# School Library Web Routes
# ====================

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backup.dependencies import get_db
from backup.modules.school.library.repository import LibraryRepository
from backup.modules.school.library.service import LibraryService

router = APIRouter(prefix="/library", tags=["School Library Web"])


def get_service(db: AsyncSession = Depends(get_db)) -> LibraryService:
    repository = LibraryRepository(db)
    return LibraryService(repository)


@router.get("/dashboard", response_class=HTMLResponse)
async def library_dashboard(
    request: Request,
    service: LibraryService = Depends(get_service)
):
    """Library dashboard page"""
    summary = await service.get_library_summary()
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>School Library Management</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .stat { display: inline-block; margin: 10px 20px; }
            h2 { color: #333; }
        </style>
    </head>
    <body>
        <h1>School Library Management</h1>
        <div class="card">
            <h2>Library Summary</h2>
            <div class="stat"><strong>Total Books:</strong> """ + str(summary.get('total_books', 0)) + """</div>
            <div class="stat"><strong>Total Copies:</strong> """ + str(summary.get('total_copies', 0)) + """</div>
            <div class="stat"><strong>Available:</strong> """ + str(summary.get('available_copies', 0)) + """</div>
            <div class="stat"><strong>Books Issued:</strong> """ + str(summary.get('books_issued', 0)) + """</div>
            <div class="stat"><strong>Overdue:</strong> """ + str(summary.get('overdue_books', 0)) + """</div>
        </div>
    </body>
    </html>
    """
    return html


@router.get("/books", response_class=HTMLResponse)
async def list_books_web(
    request: Request,
    search: Optional[str] = None,
    category: Optional[str] = None,
    service: LibraryService = Depends(get_service)
):
    """List books page"""
    books = await service.list_books(search=search, category=category, limit=50)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Book List</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #2196F3; color: white; }
        </style>
    </head>
    <body>
        <h1>Book Collection</h1>
        <table>
            <tr><th>ID</th><th>ISBN</th><th>Title</th><th>Author</th><th>Category</th><th>Available</th></tr>
    """
    
    for book in books:
        html += f"""
            <tr>
                <td>{book.get('id', '')}</td>
                <td>{book.get('isbn', '')}</td>
                <td>{book.get('title', '')}</td>
                <td>{book.get('author', '')}</td>
                <td>{book.get('category', '')}</td>
                <td>{book.get('available_copies', 0)}</td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    return html


__all__ = ["router"]
