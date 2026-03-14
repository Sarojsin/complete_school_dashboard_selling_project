"""
Create admin security tables required by user management controls.

Tables:
- login_history
- failed_login_attempts
- user_security_states
"""

import os
import sys

# Ensure project root is importable when script is run directly.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.core.database import engine
from app.models.admin_models import LoginHistory, FailedLoginAttempt, UserSecurityState


def add_admin_security_tables() -> None:
    LoginHistory.__table__.create(bind=engine, checkfirst=True)
    FailedLoginAttempt.__table__.create(bind=engine, checkfirst=True)
    UserSecurityState.__table__.create(bind=engine, checkfirst=True)
    print("Admin security tables created/verified successfully.")


if __name__ == "__main__":
    add_admin_security_tables()
