"""Assignment service (Member 5).

Pure business logic for matching sponsors and mentors to students.
No terminal I/O lives here - see menus/assignment_menu.py for the
interactive CLI layer that calls these functions.

Duplicate prevention: SponsorAssignments has a UNIQUE(sponsor_id,
student_id) constraint and MentorAssignments has a UNIQUE(mentor_id,
student_id) constraint (see database/create_tables.py). This module
checks for an existing pair before inserting (for a friendly error
message) and also catches the database-level constraint violation as
a fallback, so a duplicate can never be created even under a race.
"""

from datetime import date

from mysql.connector import Error as MySQLError

from database.connection import db
from models.student import Student
from models.sponsor import Sponsor
from models.mentor import Mentor


def list_students():
    """Return every registered student as a list of Student objects."""
    rows = db.fetch_all("SELECT * FROM Students ORDER BY student_id")
    return [Student.from_row(row) for row in rows]


def list_sponsors():
    """Return every registered sponsor as a list of Sponsor objects."""
    rows = db.fetch_all("SELECT * FROM Sponsors ORDER BY sponsor_id")
    return [Sponsor.from_row(row) for row in rows]


def list_mentors():
    """Return every registered mentor as a list of Mentor objects."""
    rows = db.fetch_all("SELECT * FROM Mentors ORDER BY mentor_id")
    return [Mentor.from_row(row) for row in rows]


def sponsor_assignment_exists(sponsor_id, student_id):
    """Return True if this exact sponsor-student pair is already assigned."""
    row = db.fetch_one(
        "SELECT assignment_id FROM SponsorAssignments "
        "WHERE sponsor_id = %s AND student_id = %s",
        (sponsor_id, student_id),
    )
    return row is not None


def mentor_assignment_exists(mentor_id, student_id):
    """Return True if this exact mentor-student pair is already assigned."""
    row = db.fetch_one(
        "SELECT assignment_id FROM MentorAssignments "
        "WHERE mentor_id = %s AND student_id = %s",
        (mentor_id, student_id),
    )
    return row is not None


def create_sponsor_assignment(sponsor_id, student_id):
    """
    Assign a sponsor to a student.

    Raises:
        ValueError: if this pair is already assigned, or the IDs don't
                    refer to real records (foreign key violation).
    """
    if sponsor_assignment_exists(sponsor_id, student_id):
        raise ValueError("This sponsor is already assigned to this student.")
    try:
        return db.execute(
            "INSERT INTO SponsorAssignments (sponsor_id, student_id, date_assigned) "
            "VALUES (%s, %s, %s)",
            (sponsor_id, student_id, date.today().isoformat()),
            commit=True,
        )
    except MySQLError as exc:
        raise ValueError(
            "Could not create this sponsorship. It may already exist, or "
            f"one of the IDs is invalid. ({exc})"
        ) from exc


def create_mentor_assignment(mentor_id, student_id):
    """
    Assign a mentor to a student.

    Raises:
        ValueError: if this pair is already assigned, or the IDs don't
                    refer to real records (foreign key violation).
    """
    if mentor_assignment_exists(mentor_id, student_id):
        raise ValueError("This mentor is already assigned to this student.")
    try:
        return db.execute(
            "INSERT INTO MentorAssignments (mentor_id, student_id, date_assigned) "
            "VALUES (%s, %s, %s)",
            (mentor_id, student_id, date.today().isoformat()),
            commit=True,
        )
    except MySQLError as exc:
        raise ValueError(
            "Could not create this mentor assignment. It may already exist, "
            f"or one of the IDs is invalid. ({exc})"
        ) from exc


def list_sponsor_assignments():
    """Return all sponsorships with readable student/sponsor names."""
    return db.fetch_all("""
        SELECT sa.assignment_id, s.fullname AS student_name,
               sp.fullname AS sponsor_name, sa.date_assigned
        FROM SponsorAssignments sa
        JOIN Students s ON sa.student_id = s.student_id
        JOIN Sponsors sp ON sa.sponsor_id = sp.sponsor_id
        ORDER BY sa.assignment_id
    """)


def list_mentor_assignments():
    """Return all mentor assignments with readable student/mentor names."""
    return db.fetch_all("""
        SELECT ma.assignment_id, s.fullname AS student_name,
               m.fullname AS mentor_name, ma.date_assigned
        FROM MentorAssignments ma
        JOIN Students s ON ma.student_id = s.student_id
        JOIN Mentors m ON ma.mentor_id = m.mentor_id
        ORDER BY ma.assignment_id
    """)


def delete_sponsor_assignment(assignment_id):
    """Remove a sponsorship by its assignment_id. Raises ValueError if missing."""
    affected = db.execute(
        "DELETE FROM SponsorAssignments WHERE assignment_id = %s",
        (assignment_id,),
        commit=True,
    )
    if not affected:
        raise ValueError("No sponsorship found with that ID.")


def delete_mentor_assignment(assignment_id):
    """Remove a mentor assignment by its assignment_id. Raises ValueError if missing."""
    affected = db.execute(
        "DELETE FROM MentorAssignments WHERE assignment_id = %s",
        (assignment_id,),
        commit=True,
    )
    if not affected:
        raise ValueError("No mentor assignment found with that ID.")
