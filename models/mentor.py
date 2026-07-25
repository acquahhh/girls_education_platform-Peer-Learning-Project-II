"""Mentor domain model."""


class Mentor:
    """Represents a professional mentor guiding students."""

    def __init__(self, fullname, profession, email, phone, mentor_id=None):
        """Initialize a Mentor record."""
        self.mentor_id = mentor_id
        self.fullname = fullname
        self.profession = profession
        self.email = email
        self.phone = phone

    @classmethod
    def from_row(cls, row):
        """Build a Mentor from a database dict row."""
        if not row:
            return None
        return cls(
            mentor_id=row.get("mentor_id"),
            fullname=row.get("fullname"),
            profession=row.get("profession"),
            email=row.get("email"),
            phone=row.get("phone"),
        )