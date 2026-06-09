from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """
    Domain model for a system user.
    DEV-3: Extended schema with role and created_at for migration v1.0.0.
    """
    username: str
    email: str
    hashed_password: str
    role: str = "viewer"                        # New field added in v1.0.0 migration
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    def deactivate(self) -> None:
        self.is_active = False

    def promote_to_admin(self) -> None:
        self.role = "admin"

    def record_login(self) -> None:
        self.last_login = datetime.utcnow()