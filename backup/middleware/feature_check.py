"""
Feature Check Middleware - Backward Compatibility Layer

This file now imports from app.shared.middleware for backward compatibility.
New code should import directly from app.shared.middleware
"""

# Re-export from shared location for backward compatibility
from backup.shared.middleware.feature_check import (
    require_feature,
    require_feature_optional,
    is_feature_enabled,
    FeatureChecker,
    Features,
)

__all__ = [
    "require_feature",
    "require_feature_optional", 
    "is_feature_enabled",
    "FeatureChecker",
    "Features",
]
