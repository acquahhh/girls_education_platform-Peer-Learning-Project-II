"""Sponsor service: CRUD operations for sponsors."""

from database.connection import db
from models.sponsor import Sponsor


def register_sponsor(fullname, organization, email, phone):
    """Insert a new sponsor. Returns True on success."""
    query = """
        INSERT INTO Sponsors (fullname, organization, email, phone)
        VALUES (%s, %s, %s, %s)
    """
    try:
        db.execute(query, (fullname, organization, email, phone), commit=True)
        return True
    except Exception as exc:
        print(f"[!] Service Error: Could not register sponsor. {exc}")
        return False


def get_all_sponsors():
    """Return all sponsors as a list of Sponsor objects."""
    query = "SELECT * FROM Sponsors"
    try:
        rows = db.fetch_all(query)
        return [Sponsor.from_row(row) for row in rows]
    except Exception as exc:
        print(f"[!] Service Error: Could not fetch sponsors. {exc}")
        return []


def search_sponsors(search_term):
    """Search sponsors by ID or name. Returns a list of Sponsor objects."""
    query = "SELECT * FROM Sponsors WHERE sponsor_id = %s OR fullname LIKE %s"
    like_term = f"%{search_term}%"
    try:
        rows = db.fetch_all(query, (search_term, like_term))
        return [Sponsor.from_row(row) for row in rows]
    except Exception as exc:
        print(f"[!] Service Error: Search failed. {exc}")
        return []


def update_sponsor_record(sponsor_id, fullname, organization, email, phone):
    """Update an existing sponsor. Returns True if a row changed."""
    query = """
        UPDATE Sponsors
        SET fullname = %s, organization = %s, email = %s, phone = %s
        WHERE sponsor_id = %s
    """
    try:
        rows_affected = db.execute(
            query, (fullname, organization, email, phone, sponsor_id),
            commit=True
        )
        return rows_affected > 0
    except Exception as exc:
        print(f"[!] Service Error: Update failed. {exc}")
        return False


def delete_sponsor_record(sponsor_id):
    """Delete a sponsor by ID. Returns True if a row was removed."""
    query = "DELETE FROM Sponsors WHERE sponsor_id = %s"
    try:
        rows_affected = db.execute(query, (sponsor_id,), commit=True)
        return rows_affected > 0
    except Exception as exc:
        print(f"[!] Service Error: Deletion failed. {exc}")
        return False