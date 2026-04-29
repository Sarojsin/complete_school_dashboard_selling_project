"""
Feature Guard - Module-level Feature Toggle System

This module provides dependency injection for enabling/disabling modules
via the Feature table in the database.

Usage:
    from modules.shared.feature_guard import require_feature
    
    @router.get("/students/", dependencies=[Depends(require_feature("school_student"))])
    def list_students(db: Session = Depends(get_db)):
        ...
"""

from fastapi import HTTPException, Depends, Request
from sqlalchemy.orm import Session
from functools import wraps
from typing import Callable, Optional
import logging

logger = logging.getLogger(__name__)


def get_db_from_request(request: Request) -> Session:
    """
    Extract database session from request state.
    This works with the standard FastAPI dependency injection.
    """
    # Try to get db from app.state or request.state
    if hasattr(request.state, 'db'):
        return request.state.db
    
    # Alternative: create a new session
    from modules.shared.database import get_db, SessionLocal
    return SessionLocal()


def check_feature(feature_name: str, db: Session) -> bool:
    """
    Check if a feature is enabled in the database.
    
    Args:
        feature_name: Name of the feature to check
        db: Database session
        
    Returns:
        bool: True if feature is enabled, False otherwise
    """
    try:
        # Import here to avoid circular imports
        from modules.super_admin.models import Feature
        
        feature = db.query(Feature).filter(Feature.name == feature_name).first()
        
        # If feature doesn't exist, default to enabled (for backwards compatibility)
        if feature is None:
            logger.warning(f"Feature '{feature_name}' not found in database. Defaulting to enabled.")
            return True
            
        return feature.is_enabled
    except Exception as e:
        logger.error(f"Error checking feature '{feature_name}': {e}")
        # Default to enabled if there's an error
        return True


def require_feature(feature_name: str):
    """
    Dependency factory that creates a FastAPI dependency to check if a feature is enabled.
    
    Usage:
        @router.get("/students/", dependencies=[Depends(require_feature("school_student"))])
        def list_students(db: Session = Depends(get_db)):
            ...
    
    Args:
        feature_name: Name of the feature that must be enabled
        
    Returns:
        A FastAPI dependency that raises 503 if feature is disabled
    """
    def checker(request: Request):
        """Dependency that checks if the feature is enabled."""
        from modules.shared.database import get_db, SessionLocal
        from modules.super_admin.models import Feature
        
        db = SessionLocal()
        try:
            feature = db.query(Feature).filter(Feature.name == feature_name).first()
            
            if feature and not feature.is_enabled:
                raise HTTPException(
                    status_code=503,
                    detail=f"Module '{feature_name}' is currently disabled. "
                           f"Please contact administrator to enable it."
                )
            
            # Feature doesn't exist - allow access (backwards compatibility)
            return True
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error checking feature '{feature_name}': {e}")
            # Default to enabled if there's a database error
            return True
        finally:
            db.close()
    
    return checker


def get_enabled_features(db: Session) -> list:
    """
    Get list of all enabled features.
    
    Args:
        db: Database session
        
    Returns:
        List of enabled feature names
    """
    try:
        from modules.super_admin.models import Feature
        
        features = db.query(Feature).filter(Feature.is_enabled == True).all()
        return [f.name for f in features]
    except Exception as e:
        logger.error(f"Error getting enabled features: {e}")
        return []


def set_feature(feature_name: str, is_enabled: bool, db: Session) -> bool:
    """
    Enable or disable a feature.
    
    Args:
        feature_name: Name of the feature
        is_enabled: Whether the feature should be enabled
        db: Database session
        
    Returns:
        True if successful, False otherwise
    """
    try:
        from modules.super_admin.models import Feature
        
        feature = db.query(Feature).filter(Feature.name == feature_name).first()
        
        if feature:
            feature.is_enabled = is_enabled
            db.commit()
            logger.info(f"Feature '{feature_name}' set to {is_enabled}")
            return True
        else:
            # Create new feature if it doesn't exist
            feature = Feature(name=feature_name, is_enabled=is_enabled)
            db.add(feature)
            db.commit()
            logger.info(f"Created feature '{feature_name}' with is_enabled={is_enabled}")
            return True
    except Exception as e:
        logger.error(f"Error setting feature '{feature_name}': {e}")
        db.rollback()
        return False


def init_default_features(db: Session):
    """
    Initialize default features for all modules.
    Call this during application startup to ensure all features exist.
    
    Args:
        db: Database session
    """
    from modules.super_admin.models import Feature
    
    default_features = [
        # School modules
        ("school_authority", True, "School authority management"),
        ("school_teacher", True, "Teacher management"),
        ("school_student", True, "Student management"),
        ("school_parent", True, "Parent portal"),
        ("school_exam_section", True, "Exam section"),
        ("school_account_section", True, "Account section"),
        ("school_library", True, "Library management"),
        ("school_attendance", True, "Attendance tracking"),
        
        # College modules
        ("college_faculty", True, "College faculty"),
        ("college_student", True, "College student"),
        ("college_hod", True, "HOD management"),
        ("college_registrar", True, "Registrar module"),
        ("college_exam_section", True, "College exam section"),
        ("college_account_section", True, "College account section"),
        ("college_library", True, "College library"),
        ("college_placement", True, "Placement cell"),
        ("college_research", True, "Research module"),
        ("college_hostel", True, "Hostel management"),
        ("college_lab", True, "Laboratory management"),
        ("college_dean", True, "Dean office"),
        
        # Core features
        ("chat", True, "Real-time chat"),
        ("groups", True, "Group discussions"),
        ("notices", True, "Notice board"),
        ("notifications", True, "Push notifications"),
    ]
    
    for name, enabled, description in default_features:
        existing = db.query(Feature).filter(Feature.name == name).first()
        if not existing:
            feature = Feature(name=name, is_enabled=enabled)
            db.add(feature)
            logger.info(f"Created default feature: {name}")
    
    db.commit()
    logger.info(f"Initialized {len(default_features)} default features")


class FeatureGuard:
    """
    Class-based feature guard for more complex scenarios.
    
    Usage:
        guard = FeatureGuard(db)
        
        if guard.is_enabled("school_student"):
            # Show student features
            ...
    """
    
    def __init__(self, db: Session):
        self.db = db
        self._cache = {}
    
    def is_enabled(self, feature_name: str) -> bool:
        """Check if a feature is enabled (with simple caching)."""
        if feature_name in self._cache:
            return self._cache[feature_name]
        
        enabled = check_feature(feature_name, self.db)
        self._cache[feature_name] = enabled
        return enabled
    
    def clear_cache(self):
        """Clear the feature cache."""
        self._cache = {}
    
    def get_enabled_modules(self) -> list:
        """Get list of all enabled module names."""
        return get_enabled_features(self.db)
