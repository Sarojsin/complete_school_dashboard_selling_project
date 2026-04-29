"""
Super Admin Module - System-wide control, dashboard, reports, settings, backups

This module provides administrative functionality for the entire system.
"""

from modules.super_admin.api import router

__all__ = ["router"]