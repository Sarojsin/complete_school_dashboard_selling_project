# College Account Section Web Routes
# ===================================

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backup.dependencies import get_db
from backup.modules.college.account_section.repository import AccountSectionRepository
from backup.modules.college.account_section.service import AccountSectionService

router = APIRouter(prefix="/account-section", tags=["College Account Section Web"])


def get_service(db: AsyncSession = Depends(get_db)) -> AccountSectionService:
    repository = AccountSectionRepository(db)
    return AccountSectionService(repository)


@router.get("/dashboard", response_class=HTMLResponse)
async def account_dashboard(
    request: Request,
    service: AccountSectionService = Depends(get_service)
):
    """Account section dashboard page"""
    summary = await service.get_financial_summary()
    
    staff = await service.get_all_staff(limit=5)
    recent_payments = await service.get_all_payments(limit=10)
    recent_expenses = await service.get_all_expenses(limit=10)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>College Account Section</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .summary {{ display: flex; gap: 20px; margin-bottom: 20px; }}
            .card {{ border: 1px solid #ddd; padding: 15px; border-radius: 5px; flex: 1; }}
            .income {{ background-color: #d4edda; }}
            .expense {{ background-color: #f8d7da; }}
            .balance {{ background-color: #cce5ff; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
        </style>
    </head>
    <body>
        <h1>College Account Section Dashboard</h1>
        
        <div class="summary">
            <div class="card income">
                <h3>Total Income</h3>
                <p>Rs. {summary.get('total_income', 0):,.2f}</p>
            </div>
            <div class="card expense">
                <h3>Total Expenses</h3>
                <p>Rs. {summary.get('total_expense', 0):,.2f}</p>
            </div>
            <div class="card balance">
                <h3>Balance</h3>
                <p>Rs. {summary.get('balance', 0):,.2f}</p>
            </div>
        </div>
        
        <h2>Recent Payments</h2>
        <table>
            <tr><th>ID</th><th>Amount</th><th>Date</th><th>Mode</th></tr>
    """
    
    for payment in recent_payments[:5]:
        p = payment.get('payment', {})
        html += f"<tr><td>{p.get('id', '')}</td><td>Rs. {p.get('amount', 0)}</td><td>{p.get('payment_date', '')}</td><td>{p.get('payment_mode', '')}</td></tr>"
    
    html += """
        </table>
        
        <h2>Recent Expenses</h2>
        <table>
            <tr><th>ID</th><th>Amount</th><th>Category</th><th>Date</th></tr>
    """
    
    for exp in recent_expenses[:5]:
        e = exp.get('expense', {})
        html += f"<tr><td>{e.get('id', '')}</td><td>Rs. {e.get('amount', 0)}</td><td>{e.get('category', '')}</td><td>{e.get('expense_date', '')}</td></tr>"
    
    html += """
        </table>
        
        <h2>Account Staff</h2>
        <table>
            <tr><th>ID</th><th>Name</th><th>Designation</th><th>Phone</th></tr>
    """
    
    for s in staff[:5]:
        st = s.get('staff', {})
        html += f"<tr><td>{st.get('id', '')}</td><td>{st.get('full_name', '')}</td><td>{st.get('designation', '')}</td><td>{st.get('phone', '')}</td></tr>"
    
    html += """
        </table>
    </body>
    </html>
    """
    return html


__all__ = ["router"]
