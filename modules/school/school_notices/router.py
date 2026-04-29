from .api import router

# Add prefix for notices
router.prefix = "/notices"

__all__ = ["router"]