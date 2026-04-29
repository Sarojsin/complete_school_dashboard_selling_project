from .api import router

# Add prefix for tests
router.prefix = "/tests"

__all__ = ["router"]