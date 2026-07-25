"""Report service (integrates Member 6's reporting logic).

Aggregate statistics across the platform. Rewritten to use the shared
database layer and the project's actual schema (sponsorship is derived
from the SponsorAssignments table, not a status column).
"""

from database.connection import db


def count_students():
    """Return the total number of registered students."""
    return db.fetch_scalar("SELECT COUNT(*) FROM Students") or 0


def count_sponsors():
    """Return the total number of registered sponsors."""
    return db.fetch_scalar("SELECT COUNT(*) FROM Sponsors") or 0


def count_mentors():
    """Return the total number of registered mentors."""
    return db.fetch_scalar("SELECT COUNT(*) FROM Mentors") or 0


def count_sponsored_students():
    """Return how many students have at least one sponsor assigned."""
    return db.fetch_scalar(
        "SELECT COUNT(DISTINCT student_id) FROM SponsorAssignments"
    ) or 0


def count_unsponsored_students():
    """Return how many students have no sponsor yet."""
    return count_students() - count_sponsored_students()


def count_mentor_assignments():
    """Return how many students have a mentor assigned."""
    return db.fetch_scalar(
        "SELECT COUNT(DISTINCT student_id) FROM MentorAssignments"
    ) or 0


def generate_summary_report():
    """Return a dict of all summary metrics for display."""
    total_students = count_students()
    sponsored = count_sponsored_students()

    if total_students > 0:
        rate = round((sponsored / total_students) * 100, 1)
    else:
        rate = 0.0

    return {
        "total_students": total_students,
        "sponsored": sponsored,
        "unsponsored": total_students - sponsored,
        "sponsorship_rate": rate,
        "total_sponsors": count_sponsors(),
        "total_mentors": count_mentors(),
        "mentor_assignments": count_mentor_assignments(),
    }