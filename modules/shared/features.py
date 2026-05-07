"""
Feature Flags System

Provides runtime toggling of application features without requiring code deployments.
Features can be enabled/disabled via environment variables for gradual rollouts,
A/B testing, and operational control.
"""

import os
from typing import Dict, Any


class FeatureFlags:
    """
    Centralized feature flag management.

    All feature flags are controlled via environment variables and can be
    toggled at runtime without restarting the application.
    """

    # College Module Features
    COLLEGE_FACULTY = _get_bool_env("FEATURE_COLLEGE_FACULTY", True)
    COLLEGE_STUDENTS = _get_bool_env("FEATURE_COLLEGE_STUDENTS", True)
    COLLEGE_COURSES = _get_bool_env("FEATURE_COLLEGE_COURSES", True)
    COLLEGE_PROGRAMS = _get_bool_env("FEATURE_COLLEGE_PROGRAMS", True)
    COLLEGE_ENROLLMENTS = _get_bool_env("FEATURE_COLLEGE_ENROLLMENTS", True)
    COLLEGE_EXAM_SECTION = _get_bool_env("FEATURE_COLLEGE_EXAM_SECTION", True)
    COLLEGE_ACCOUNT_SECTION = _get_bool_env("FEATURE_COLLEGE_ACCOUNT_SECTION", True)
    COLLEGE_HOSTEL = _get_bool_env("FEATURE_COLLEGE_HOSTEL", True)
    COLLEGE_LAB = _get_bool_env("FEATURE_COLLEGE_LAB", True)
    COLLEGE_RESEARCH = _get_bool_env("FEATURE_COLLEGE_RESEARCH", True)
    COLLEGE_PLACEMENT = _get_bool_env("FEATURE_COLLEGE_PLACEMENT", True)

    # School Module Features
    SCHOOL_CORE = _get_bool_env("FEATURE_SCHOOL_CORE", True)
    SCHOOL_LIBRARY = _get_bool_env("FEATURE_SCHOOL_LIBRARY", True)
    SCHOOL_EXAM = _get_bool_env("FEATURE_SCHOOL_EXAM", True)
    SCHOOL_ATTENDANCE = _get_bool_env("FEATURE_SCHOOL_ATTENDANCE", True)
    SCHOOL_TRANSPORT = _get_bool_env("FEATURE_SCHOOL_TRANSPORT", True)
    SCHOOL_CANTEEN = _get_bool_env("FEATURE_SCHOOL_CANTEEN", True)
    SCHOOL_GROUPS = _get_bool_env("FEATURE_SCHOOL_GROUPS", True)
    SCHOOL_ASSESSMENTS = _get_bool_env("FEATURE_SCHOOL_ASSESSMENTS", True)

    # Security Features
    RATE_LIMITING = _get_bool_env("FEATURE_RATE_LIMITING", True)
    AUDIT_LOGGING = _get_bool_env("FEATURE_AUDIT_LOGGING", True)
    SOFT_DELETE = _get_bool_env("FEATURE_SOFT_DELETE", True)

    # Monitoring Features
    PROMETHEUS_METRICS = _get_bool_env("FEATURE_PROMETHEUS_METRICS", True)
    SENTRY_TRACKING = _get_bool_env("FEATURE_SENTRY_TRACKING", True)
    HEALTH_CHECKS = _get_bool_env("FEATURE_HEALTH_CHECKS", True)

    # Advanced Features
    NOTIFICATIONS = _get_bool_env("FEATURE_NOTIFICATIONS", False)
    REPORTING = _get_bool_env("FEATURE_REPORTING", False)
    ANALYTICS = _get_bool_env("FEATURE_ANALYTICS", False)

    @classmethod
    def get_all_flags(cls) -> Dict[str, bool]:
        """
        Get all feature flags as a dictionary.

        Returns:
            Dictionary mapping flag names to boolean values
        """
        return {
            name: getattr(cls, name)
            for name in dir(cls)
            if not name.startswith('_') and isinstance(getattr(cls, name), bool)
        }

    @classmethod
    def is_enabled(cls, feature_name: str) -> bool:
        """
        Check if a specific feature is enabled.

        Args:
            feature_name: Name of the feature flag (without FEATURE_ prefix)

        Returns:
            True if feature is enabled, False otherwise
        """
        full_name = f"FEATURE_{feature_name.upper()}"
        return getattr(cls, full_name, False)

    @classmethod
    def get_enabled_features(cls) -> list[str]:
        """
        Get list of all enabled features.

        Returns:
            List of enabled feature names
        """
        return [
            name for name, enabled in cls.get_all_flags().items()
            if enabled
        ]

    @classmethod
    def get_disabled_features(cls) -> list[str]:
        """
        Get list of all disabled features.

        Returns:
            List of disabled feature names
        """
        return [
            name for name, enabled in cls.get_all_flags().items()
            if not enabled
        ]

    @classmethod
    def reload_flags(cls):
        """
        Reload all feature flags from environment variables.

        Useful for runtime flag updates without restarting the application.
        """
        # Re-evaluate all boolean environment variables
        for attr_name in dir(cls):
            if attr_name.startswith('FEATURE_'):
                env_var = attr_name
                default_value = getattr(cls, attr_name, True)
                setattr(cls, attr_name, _get_bool_env(env_var, default_value))


def _get_bool_env(env_var: str, default: bool = False) -> bool:
    """
    Get boolean value from environment variable.

    Args:
        env_var: Environment variable name
        default: Default value if not set or invalid

    Returns:
        Boolean value
    """
    value = os.getenv(env_var)
    if value is None:
        return default

    # Convert string to boolean
    value_lower = value.lower().strip()
    if value_lower in ('true', '1', 'yes', 'on', 'enabled'):
        return True
    elif value_lower in ('false', '0', 'no', 'off', 'disabled'):
        return False
    else:
        # Invalid value, use default
        return default


# Feature flag groups for easier management
COLLEGE_FEATURES = [
    'COLLEGE_FACULTY', 'COLLEGE_STUDENTS', 'COLLEGE_COURSES',
    'COLLEGE_PROGRAMS', 'COLLEGE_ENROLLMENTS', 'COLLEGE_EXAM_SECTION',
    'COLLEGE_ACCOUNT_SECTION', 'COLLEGE_HOSTEL', 'COLLEGE_LAB',
    'COLLEGE_RESEARCH', 'COLLEGE_PLACEMENT'
]

SCHOOL_FEATURES = [
    'SCHOOL_CORE', 'SCHOOL_LIBRARY', 'SCHOOL_EXAM', 'SCHOOL_ATTENDANCE',
    'SCHOOL_TRANSPORT', 'SCHOOL_CANTEEN', 'SCHOOL_GROUPS', 'SCHOOL_ASSESSMENTS'
]

SECURITY_FEATURES = [
    'RATE_LIMITING', 'AUDIT_LOGGING', 'SOFT_DELETE'
]

MONITORING_FEATURES = [
    'PROMETHEUS_METRICS', 'SENTRY_TRACKING', 'HEALTH_CHECKS'
]

ADVANCED_FEATURES = [
    'NOTIFICATIONS', 'REPORTING', 'ANALYTICS'
]

__all__ = [
    'FeatureFlags',
    'COLLEGE_FEATURES',
    'SCHOOL_FEATURES',
    'SECURITY_FEATURES',
    'MONITORING_FEATURES',
    'ADVANCED_FEATURES'
]