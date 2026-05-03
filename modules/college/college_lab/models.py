"""
College Lab Models

Models for lab management - Lab, Equipment, Schedule.
All models are imported from backup.models.college.lab for single source of truth.
"""

from backup.models.college.lab import Lab, LabEquipment, LabSchedule

__all__ = ["Lab", "LabEquipment", "LabSchedule"]
