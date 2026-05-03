"""
College Research Models

Models for research management - ResearchProject, Publication, Patent.
All models are imported from backup.models.college.research for single source of truth.
"""

from backup.models.college.research import ResearchProject, Publication, Patent

__all__ = ["ResearchProject", "Publication", "Patent"]
