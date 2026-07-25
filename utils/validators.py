"""Input validation helpers.

Each validator raises ValueError with a clear message on invalid input so
that callers can surface friendly errors to the user.
"""

import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN = re.compile(r"^\+?\d[\d\s-]{6,19}$")


def validate_non_empty(value, field_name):
    """Ensure a string field is not empty or whitespace only."""
    if value is None or not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")
    return value.strip()


def validate_age(value):
    """Validate that age is an integer within a sensible school range."""
    try:
        age = int(value)
    except (TypeError, ValueError):
        raise ValueError("Age must be a whole number.")
    if not 3 <= age <= 30:
        raise ValueError("Age must be between 3 and 30.")
    return age


def validate_email(value):
    """Validate an email address format."""
    value = validate_non_empty(value, "Email")
    if not EMAIL_PATTERN.match(value):
        raise ValueError("Email format is invalid.")
    return value


def validate_phone(value):
    """Validate a phone number format."""
    value = validate_non_empty(value, "Phone")
    if not PHONE_PATTERN.match(value):
        raise ValueError("Phone number format is invalid.")
    return value


def validate_role(value):
    """Validate that a role is one of the allowed values."""
    value = validate_non_empty(value, "Role").lower()
    if value not in ("admin", "staff"):
        raise ValueError("Role must be either 'admin' or 'staff'.")
    return value


def validate_positive_int(value, field_name):
    """Validate that a value is a positive integer id."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a whole number.")
    if number <= 0:
        raise ValueError(f"{field_name} must be a positive number.")
    return number