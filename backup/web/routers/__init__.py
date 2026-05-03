from backup.web.routers.common import router as common_router
from backup.web.routers.student import router as student_router
from backup.web.routers.teacher import router as teacher_router
from backup.web.routers.parent import router as parent_router
from backup.web.routers.authority import router as authority_router
from backup.web.routers.groups import router as groups_router

__all__ = [
    "common_router",
    "student_router",
    "teacher_router",
    "parent_router",
    "authority_router",
    "groups_router",
]
