# School Account Section Web Routes
# ==============================

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backup.dependencies import get_db
from backup.modules.school.account_section.repository import AccountSectionRepository
from backup.modules.school.account_section.service import AccountSectionService

router = APIRouter(prefix="/account", tags=["School Account Web"])


def get_service(db: AsyncSession = Depends(get_db)) -> AccountSectionService:
    repository = AccountSectionRepository(db)
    return AccountSectionService(repository)


@router.get("/dashboard", response_class=HTMLResponse)
async def account_dashboard(
    request: Request,
    service: AccountSectionService = Depends(get_service)
):
    """Account management dashboard page"""
    summary = await service.get_financial_summary()
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>School Account Management</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .stat { display: inline-block; margin: 10px 20px; }
            h2 { color: #333; }
        </style>
    </head>
    <body>
        <h1>School Account Management</h1>
        <div class="card">
            <h2>Financial Summary</h2>
            <div class="stat"><strong>Total Fees Collected:</strong> $""" + f"{summary.get('total_fees_collected', 0):,.2f}" + """</div>
            <div class="stat"><strong>Total Fees Pending:</strong> $""" + f"{summary.get('total_fees_pending', 0):,.2f}" + """</div>
            <div class="stat"><strong>Total Expenses:</strong> $""" + f"{summary.get('total_expenses', 0):,.2f}" + """</div>
            <div class="stat"><strong>Net Balance:</strong> $""" + f"{summary.get('net_balance', 0):,.2f}" + """</div>
        </div>
        <div class="card">
            <h2>Payment Status</h2>
            <div class="stat"><strong>Paid Students:</strong> """ + str(summary.get('paid_students', 0)) + """</div>
            <div class="stat"><strong>Pending Students:</strong> """ + str(summary.get('pending_students', 0)) + """</div>
        </div>
    </body>
    </html>
    """
    return html


@router.get("/fees", response_class=HTMLResponse)
async def list_fees_web(
    request: Request,
    student_id: Optional[int] = None,
    service: AccountSectionService = Depends(get_service)
):
    """List fees page"""
    fees = await service.list_fees(student_id=student_id, limit=50)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fee List</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
        </style>
    </head>
    <body>
        <h1>Fee List</h1>
        <table>
            <tr><th>ID</th><th>Student ID</th><th>Fee Type</th><th>Amount</th><th>Paid</th><th>Status</th></tr>
    """
    
    for fee in fees:
        html += f"""
            <tr>
                <td>{fee.get('id', '')}</td>
                <td>{fee.get('student_id', '')}</td>
                <td>{fee.get('fee_type', '')}</td>
                <td>${fee.get('amount', 0):,.2f}</td>
                <td>${fee.get('paid_amount', 0):,.2f}</td>
                <td>{fee.get('payment_status', '')}</td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    return html


@router.get("/expenses", response_class=HTMLResponse)
async def list_expenses_web(
    request: Request,
    category: Optional[str] = None,
    service: AccountSectionService = Depends(get_service)
):
    """List expenses page"""
    expenses = await service.list_expenses(category=category, limit=50)
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Expense List</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #FF5722; color: white; }
        </style>
    </head>
    <body>
        <h1>Expense List</h1>
        <table>
            <tr><th>ID</th><th>Category</th><th>Amount</th><th>Date</th><th>Vendor</th></tr>
    """
    
    for expense in expenses:
        html += f"""
            <tr>
                <td>{expense.get('id', '')}</td>
                <td>{expense.get('category', '')}</td>
                <td>${expense.get('amount', 0):,.2f}</td>
                <td>{expense.get('expense_date', '')}</td>
                <td>{expense.get('vendor', 'N/A')}</td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    return html


__all__ = ["router"]
