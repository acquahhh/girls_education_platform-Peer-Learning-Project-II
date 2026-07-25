"""General-purpose helpers for the CLI and security.

Includes password hashing (SHA-256 with per-user salt), formatted table
printing, and safe prompt utilities.
"""

import getpass
import hashlib
import os


def hash_password(password, salt=None):
    """Hash a password using SHA-256 with a random salt.

    Returns:
        str: A string of the form "salt$hash".
    """
    if salt is None:
        salt = os.urandom(16).hex()
    digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${digest}"


def verify_password(password, stored):
    """Verify a plaintext password against a stored "salt$hash" value.

    Returns:
        bool: True if the password matches, else False.
    """
    if not stored or "$" not in stored:
        return False
    salt, _ = stored.split("$", 1)
    return hash_password(password, salt) == stored


def prompt(message):
    """Prompt the user for input and strip surrounding whitespace."""
    return input(message).strip()


def prompt_password(message="Password: "):
    """Prompt for a password without echoing to the terminal."""
    return getpass.getpass(message)


def print_header(title):
    """Print a consistent, boxed section header."""
    line = "=" * 30
    print(f"\n{line}")
    print(title.center(30))
    print(line)


def print_table(rows, columns):
    """Print a list of dict rows as a simple aligned table.

    Args:
        rows (list): List of dict records.
        columns (list): Ordered list of (key, header) tuples.
    """
    if not rows:
        print("  (no records found)")
        return

    headers = [header for _, header in columns]
    keys = [key for key, _ in columns]

    widths = []
    for key, header in columns:
        longest = max(
            [len(str(row.get(key, ""))) for row in rows] + [len(header)]
        )
        widths.append(longest)

    header_line = " | ".join(
        header.ljust(widths[i]) for i, header in enumerate(headers)
    )
    print(header_line)
    print("-" * len(header_line))
    for row in rows:
        print(
            " | ".join(
                str(row.get(keys[i], "")).ljust(widths[i])
                for i in range(len(keys))
            )
        )


def pause():
    """Wait for the user to press Enter before continuing."""
    input("\nPress Enter to continue...")