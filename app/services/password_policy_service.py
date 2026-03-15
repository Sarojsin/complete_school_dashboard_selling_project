from __future__ import annotations

from typing import Dict, List

from app.core.exceptions import ValidationError
from app.repositories.admin_settings_repository import AdminSettingsRepository


DEFAULT_PASSWORD_POLICY = {
    "min_length": 8,
    "require_uppercase": True,
    "require_numbers": True,
    "require_special_chars": True,
    "expiry_days": 90,
    "prevent_reuse_count": 5,
}


class PasswordPolicyService:
    """Validate passwords against admin-configurable policy."""

    @staticmethod
    def _validate(password: str, policy: Dict[str, object]) -> List[str]:
        errors: List[str] = []
        min_length = int(policy.get("min_length", 8))
        if len(password) < min_length:
            errors.append(f"minimum length is {min_length}")

        if policy.get("require_uppercase"):
            if not any(char.isupper() for char in password):
                errors.append("must include an uppercase letter")

        if policy.get("require_numbers"):
            if not any(char.isdigit() for char in password):
                errors.append("must include a number")

        if policy.get("require_special_chars"):
            if not any(not char.isalnum() for char in password):
                errors.append("must include a special character")

        return errors

    @staticmethod
    async def enforce(db, password: str) -> Dict[str, object]:
        policy = await AdminSettingsRepository.get_setting_value(
            db, "password_policy", DEFAULT_PASSWORD_POLICY
        )
        if not isinstance(policy, dict):
            policy = dict(DEFAULT_PASSWORD_POLICY)

        errors = PasswordPolicyService._validate(password, policy)
        if errors:
            raise ValidationError("Password does not meet policy: " + "; ".join(errors))
        return policy
