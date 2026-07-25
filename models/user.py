"""User domain model."""


class User:
    """Represents an application user (admin or staff)."""

    def __init__(self, fullname, username, password, role, user_id=None):
        """Initialize a User."""
        self.id = user_id
        self.fullname = fullname
        self.username = username
        self.password = password
        self.role = role

    @classmethod
    def from_row(cls, row):
        """Build a User from a database dict row."""
        if not row:
            return None
        return cls(
            user_id=row.get("id"),
            fullname=row.get("fullname"),
            username=row.get("username"),
            password=row.get("password"),
            role=row.get("role"),
        )

    @property
    def is_admin(self):
        """Return True if the user has the admin role."""
        return self.role == "admin"