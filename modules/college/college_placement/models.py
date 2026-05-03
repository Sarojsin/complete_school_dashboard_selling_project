"""
College Placement Models

Models for placement management - Company, Job, Application.
All models are imported from backup.models.college.placement for single source of truth.
"""

from backup.models.college.placement import Company as PlacementCompany, Job as PlacementJob, Application as PlacementApplication

# Re-export with consistent naming
__all__ = ["PlacementCompany", "PlacementJob", "PlacementApplication"]
