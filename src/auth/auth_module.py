import hashlib
import hmac
from typing import Optional
from src.users.user_model import User


class AuthenticationError(Exception):
    pass


class AuthModule:
    """
    Handles user login, logout, and session validation.
    Linked to DEV-1: Add user authentication module.
    """

    def __init__(self, secret_key: str) -> None:
        self._secret_key = secret_key
        self._active_sessions: dict[str, str] = {}  # token -> username

    def login(self, username: str, password: str, user_store: dict[str, User]) -> str:
        """
        Validates credentials and returns a session token.
        Raises AuthenticationError if credentials are invalid.
        """
        user = user_store.get(username)
        if user is None:
            raise AuthenticationError(f"User '{username}' not found.")

        if not self._verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid password.")

        token = self._generate_token(username)
        self._active_sessions[token] = username
        return token

    def logout(self, token: str) -> None:
        """Invalidates the session token."""
        if token not in self._active_sessions:
            raise AuthenticationError("Session not found or already expired.")
        del self._active_sessions[token]

    def validate_session(self, token: str) -> Optional[str]:
        """Returns the username if token is valid, else None."""
        return self._active_sessions.get(token)

    def _verify_password(self, raw_password: str, hashed_password: str) -> bool:
        expected = hashlib.sha256(raw_password.encode()).hexdigest()
        return hmac.compare_digest(expected, hashed_password)

    def _generate_token(self, username: str) -> str:
        import secrets
        return secrets.token_hex(32)