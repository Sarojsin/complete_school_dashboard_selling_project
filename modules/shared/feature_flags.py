import os
from typing import Dict, Any, Optional
from enum import Enum

class FeatureFlag(Enum):
    """Enumeration of available feature flags"""
    COLLEGE_MODULE = "college_module"
    SCHOOL_MODULE = "school_module"
    ADVANCED_LOGGING = "advanced_logging"
    METRICS_ENABLED = "metrics_enabled"
    RATE_LIMITING = "rate_limiting"
    SOFT_DELETE = "soft_delete"
    AUDIT_LOGGING = "audit_logging"
    BACKUP_SYSTEM = "backup_system"

class FeatureFlags:
    """Feature flags management system for runtime toggling of application features"""

    def __init__(self):
        self._flags: Dict[str, bool] = {}
        self._load_flags()

    def _load_flags(self):
        """Load feature flags from environment variables with defaults"""
        flag_defaults = {
            FeatureFlag.COLLEGE_MODULE.value: True,
            FeatureFlag.SCHOOL_MODULE.value: True,
            FeatureFlag.ADVANCED_LOGGING.value: True,
            FeatureFlag.METRICS_ENABLED.value: True,
            FeatureFlag.RATE_LIMITING.value: True,
            FeatureFlag.SOFT_DELETE.value: True,
            FeatureFlag.AUDIT_LOGGING.value: True,
            FeatureFlag.BACKUP_SYSTEM.value: True,
        }

        for flag in FeatureFlag:
            env_var = f"FEATURE_{flag.value.upper()}"
            env_value = os.getenv(env_var)
            if env_value is not None:
                self._flags[flag.value] = env_value.lower() in ('true', '1', 'yes', 'on')
            else:
                self._flags[flag.value] = flag_defaults.get(flag.value, False)

    def is_enabled(self, flag: FeatureFlag) -> bool:
        """Check if a feature flag is enabled"""
        return self._flags.get(flag.value, False)

    def get_all_flags(self) -> Dict[str, bool]:
        """Get all feature flags and their current status"""
        return self._flags.copy()

    def enable_flag(self, flag: FeatureFlag):
        """Enable a feature flag (primarily for testing/admin purposes)"""
        self._flags[flag.value] = True

    def disable_flag(self, flag: FeatureFlag):
        """Disable a feature flag (primarily for testing/admin purposes)"""
        self._flags[flag.value] = False

    def set_flag(self, flag: FeatureFlag, enabled: bool):
        """Set a feature flag to a specific state"""
        self._flags[flag.value] = enabled

# Global feature flags instance
feature_flags = FeatureFlags()</content>
<parameter name="filePath">modules/shared/feature_flags.py