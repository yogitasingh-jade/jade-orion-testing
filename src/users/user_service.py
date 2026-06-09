import hashlib
import logging
from typing import Optional
from src.users.user_model import User

logger = logging.getLogger(__name__)


class UserService:
    """
    CRUD operations for user management.
    DEV-2: Fixed null pointer when fetching non-existent users.
    """

    def __init__(self) -> None:
        self._store: dict[str, User] = {}

    def create_user(self, username: str, email: str, raw_password: str) -> User:
        if not username or not email:
            raise ValueError("Username and email are required.")

        if username in self._store:
            raise ValueError(f"User '{username}' already exists.")

        hashed = hashlib.sha256(raw_password.encode()).hexdigest()
        user = User(username=username, email=email, hashed_password=hashed)
        self._store[username] = user
        logger.info("Created user: %s", username)
        return user

    def get_user(self, username: str) -> Optional[User]:
        """
        Previously raised KeyError for missing users (DEV-2 bug).
        Now safely returns None.
        """
        return self._store.get(username)  # Fix: was self._store[username]

    def update_email(self, username: str, new_email: str) -> User:
        user = self.get_user(username)
        if user is None:
            raise ValueError(f"Cannot update — user '{username}' not found.")
        user.email = new_email
        self._store[username] = user
        return user

    def delete_user(self, username: str) -> None:
        if username not in self._store:
            raise ValueError(f"User '{username}' does not exist.")
        del self._store[username]
        logger.info("Deleted user: %s", username)

    def list_users(self) -> list[User]:
        return list(self._store.values())