# School Exam Section Exceptions
# ==========================

class ExamSectionException(Exception):
    def __init__(self, message: str = "Exam section error"):
        self.message = message
        super().__init__(self.message)


class ExamNotFoundException(ExamSectionException):
    def __init__(self, exam_id: int):
        self.exam_id = exam_id
        super().__init__(f"Exam with ID {exam_id} not found")


class GradeNotFoundException(ExamSectionException):
    def __init__(self, grade_id: int):
        self.grade_id = grade_id
        super().__init__(f"Grade with ID {grade_id} not found")


__all__ = [
    "ExamSectionException",
    "ExamNotFoundException",
    "GradeNotFoundException",
]
