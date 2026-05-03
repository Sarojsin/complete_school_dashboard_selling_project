# College Lab Web Routes
# ===================

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backup.dependencies import get_db
from backup.modules.college.lab.repository import LabRepository
from backup.modules.college.lab.service import LabService

router = APIRouter(prefix="/labs", tags=["College Labs Web"])


def get_service(db: AsyncSession = Depends(get_db)) -> LabService:
    repository = LabRepository(db)
    return LabService(repository)


@router.get("/dashboard", response_class=HTMLResponse)
async def lab_dashboard(
    request: Request,
    service: LabService = Depends(get_service)
):
    """Lab management dashboard page"""
    labs = await service.get_all_labs(limit=20)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>College Lab Management</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .lab-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
            .lab-card { border: 1px solid #ddd; padding: 15px; border-radius: 5px; }
            .lab-header { background-color: #4CAF50; color: white; padding: 10px; margin: -15px -15px 15px -15px; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
        </style>
    </head>
    <body>
        <h1>College Lab Management</h1>
        <div class="lab-grid">
    """
    
    for lab_item in labs:
        lab = lab_item.get('lab', {})
        html += f"""
            <div class="lab-card">
                <div class="lab-header">
                    <h3>{lab.get('name', '')} ({lab.get('code', '')})</h3>
                </div>
                <p><strong>Capacity:</strong> {lab.get('capacity', 0)}</p>
                <p><strong>Location:</strong> {lab.get('location', 'N/A')}</p>
                <p><strong>Equipment:</strong> {lab.get('equipment_count', 0)}</p>
                <p><strong>Status:</strong> {'Active' if lab.get('is_active', True) else 'Inactive'}</p>
            </div>
        """
    
    html += """
        </div>
    </body>
    </html>
    """
    return html


__all__ = ["router"]
