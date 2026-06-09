import secrets
import hashlib
from datetime import datetime, timedelta


class TokenHelper:
    """
    Utility for generating and validating tokens.
    NOTE: This was refactored without a Jira ticket — will appear as orphan_alert.
    """

    TOKEN_EXPIRY_HOURS = 24

    @staticmethod
    def generate_reset_token() -> str:
        """Generates a secure password reset token."""
        return secrets.token_urlsafe(48)

    @staticmethod
    def hash_token(token: str) -> str:
        """Hashes a token before storing it in the DB."""
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def is_token_expired(created_at: datetime) -> bool:
        """Returns True if token is older than TOKEN_EXPIRY_HOURS."""
        expiry = created_at + timedelta(hours=TokenHelper.TOKEN_EXPIRY_HOURS)
        return datetime.utcnow() > expiry

    @staticmethod
    def generate_api_key(prefix: str = "sk") -> str:
        """Generates a prefixed API key e.g. sk-abc123..."""
        return f"{prefix}-{secrets.token_hex(24)}"