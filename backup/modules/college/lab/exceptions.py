# College Lab Exceptions
# ==================

class LabException(Exception):
    """Base exception for lab errors"""
    def __init__(self, message: str = "Lab error"):
        self.message = message
        super().__init__(self.message)


class LabNotFoundException(LabException):
    def __init__(self, lab_id: int):
        self.lab_id = lab_id
        super().__init__(f"Lab with ID {lab_id} not found")


class EquipmentNotFoundException(LabException):
    def __init__(self, equipment_id: int):
        self.equipment_id = equipment_id
        super().__init__(f"Equipment with ID {equipment_id} not found")


class ScheduleNotFoundException(LabException):
    def __init__(self, schedule_id: int):
        self.schedule_id = schedule_id
        super().__init__(f"Schedule with ID {schedule_id} not found")


class LabCapacityExceededException(LabException):
    def __init__(self, lab_name: str, capacity: int):
        self.lab_name = lab_name
        self.capacity = capacity
        super().__init__(f"Lab {lab_name} has reached its capacity of {capacity}")


__all__ = [
    "LabException",
    "LabNotFoundException",
    "EquipmentNotFoundException",
    "ScheduleNotFoundException",
    "LabCapacityExceededException",
]
