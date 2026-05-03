from .api import router

# Add prefix for grades
router.prefix = "/grades"

__all__ = ["router"]