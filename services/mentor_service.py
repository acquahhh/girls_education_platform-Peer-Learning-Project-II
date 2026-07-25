from database.connection import db
from models.mentor import Mentor


def register_mentor(fullname, profession, email, phone):
    query = """
        INSERT INTO mentors (fullname, profession, email, phone)
        VALUES (%s, %s, %s, %s)
    """
    try:
        db.execute(query, (fullname, profession, email, phone), commit=True)
        return True
    except Exception as exc:
        print(f"❌ Service Error: Could not register mentor. {exc}")
        return False


def get_all_mentors():
    query = "SELECT * FROM mentors"
    try:
        rows = db.fetch_all(query)
        return [Mentor.from_row(row) for row in rows]
    except Exception as exc:
        print(f"❌ Service Error: Could not fetch mentors. {exc}")
        return []


def search_mentors(search_term):
    query = "SELECT * FROM mentors WHERE mentor_id = %s OR fullname LIKE %s"
    like_term = f"%{search_term}%"
    try:
        rows = db.fetch_all(query, (search_term, like_term))
        return [Mentor.from_row(row) for row in rows]
    except Exception as exc:
        print(f"❌ Service Error: Search failed. {exc}")
        return []


def update_mentor_record(mentor_id, fullname, profession, email, phone):
    query = """
        UPDATE mentors
        SET fullname = %s, profession = %s, email = %s, phone = %s
        WHERE mentor_id = %s
    """
    try:
        rows_affected = db.execute(
            query, (fullname, profession, email, phone, mentor_id), commit=True
        )
        return rows_affected > 0
    except Exception as exc:
        print(f"❌ Service Error: Update failed. {exc}")
        return False


def delete_mentor_record(mentor_id):
    query = "DELETE FROM mentors WHERE mentor_id = %s"
    try:
        rows_affected = db.execute(query, (mentor_id,), commit=True)
        return rows_affected > 0
    except Exception as exc:
        print(f"❌ Service Error: Deletion failed. {exc}")
        return False

