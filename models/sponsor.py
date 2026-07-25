"""Sponsor domain model."""


class Sponsor:
    """Represents an individual or organization funding students."""

    def __init__(self, fullname, organization, email, phone,
                 sponsor_id=None):
        """Initialize a Sponsor record."""
        self.sponsor_id = sponsor_id
        self.fullname = fullname
        self.organization = organization
        self.email = email
        self.phone = phone

    @classmethod
    def from_row(cls, row):
        """Build a Sponsor from a database dict row."""
        if not row:
            return None
        return cls(
            sponsor_id=row.get("sponsor_id"),
            fullname=row.get("fullname"),
            organization=row.get("organization"),
            email=row.get("email"),
            phone=row.get("phone"),
        )