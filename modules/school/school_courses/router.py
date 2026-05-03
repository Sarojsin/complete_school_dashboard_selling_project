from .api import router

# Add prefix for courses
router.prefix = "/courses"

__all__ = ["router"]