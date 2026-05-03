# School Exam Section Web Routes
# ==========================

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backup.dependencies import get_db
from backup.modules.school.exam_section.repository import ExamSectionRepository
from backup.modules.school.exam_section.service import ExamSectionService

router = APIRouter(prefix="/exams", tags=["School Exams Web"])


def get_service(db: AsyncSession = Depends(get_db)) -> ExamSectionService:
    repository = ExamSectionRepository(db)
    return ExamSectionService(repository)


@router.get("/dashboard", response_class=HTMLResponse)
async def exam_dashboard(
    request: Request,
    service: ExamSectionService = Depends(get_service)
):
    """Exam management dashboard page"""
    exams = await service.get_all_exams(limit=20)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>School Exam Management</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
        </style>
    </head>
    <body>
        <h1>School Exam Management</h1>
        <h2>Upcoming Exams</h2>
        <table>
            <tr><th>ID</th><th>Subject</th><th>Date</th><th>Time</th><th>Total Marks</th></tr>
    """
    
    for exam_item in exams:
        exam = exam_item.get('exam', {})
        html += f"""
            <tr>
                <td>{exam.get('id', '')}</td>
                <td>{exam.get('subject', '')}</td>
                <td>{exam.get('exam_date', '')}</td>
                <td>{exam.get('start_time', '')} - {exam.get('end_time', '')}</td>
                <td>{exam.get('total_marks', 0)}</td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    return html


__all__ = ["router"]
