"""Seed script for demo data.

Clears existing records and loads a clean, intentional dataset so the
application can be demonstrated with realistic data already in place.

Run once before a demo:  python seed_data.py
"""

from datetime import date

from database.connection import db
from database.create_tables import create_tables


def clear_data():
    """Remove all existing rows so the demo starts from a clean slate.

    Order matters: assignment tables reference students/sponsors/mentors,
    so they are cleared first to satisfy foreign key constraints.
    """
    db.execute("DELETE FROM SponsorAssignments", commit=True)
    db.execute("DELETE FROM MentorAssignments", commit=True)
    db.execute("DELETE FROM Students", commit=True)
    db.execute("DELETE FROM Sponsors", commit=True)
    db.execute("DELETE FROM Mentors", commit=True)
    print("Existing data cleared.")


def seed_students():
    """Insert sample students."""
    students = [
        ("Abigail Cobbinah", 14, "Accra Girls SHS", "Form 2",
         "Eric Cobbinah", "+233201111111"),
        ("Amina Diallo", 12, "Kigali Primary", "Primary 6",
         "Fatou Diallo", "+250781111111"),
        ("Grace Mwangi", 15, "Nairobi Girls High", "Form 3",
         "Peter Mwangi", "+254701111111"),
        ("Zainab Ibrahim", 13, "Lagos Model School", "JSS 2",
         "Musa Ibrahim", "+234801111111"),
    ]
    for s in students:
        db.execute(
            "INSERT INTO Students (fullname, age, school, class_level, "
            "guardian_name, guardian_phone) VALUES (%s, %s, %s, %s, %s, %s)",
            s, commit=True,
        )
    print(f"Inserted {len(students)} students.")


def seed_sponsors():
    """Insert sample sponsors."""
    sponsors = [
        ("Acquah Foundation", "Acquah Foundation", "info@acquahfdn.org",
         "+250782000001"),
        ("Mastercard Foundation", "Mastercard Foundation",
         "grants@mcf.org", "+250782000002"),
        ("Jane Osei", "Independent Donor", "jane.osei@email.com",
         "+233202000003"),
    ]
    for s in sponsors:
        db.execute(
            "INSERT INTO Sponsors (fullname, organization, email, phone) "
            "VALUES (%s, %s, %s, %s)",
            s, commit=True,
        )
    print(f"Inserted {len(sponsors)} sponsors.")


def seed_mentors():
    """Insert sample mentors."""
    mentors = [
        ("Albert Afiti", "Software Engineer", "albert@email.com",
         "+233201222001"),
        ("Dr. Sarah Kimani", "Medical Doctor", "sarah.k@email.com",
         "+254702222002"),
        ("Emmanuel Boateng", "Civil Engineer", "e.boateng@email.com",
         "+233203222003"),
    ]
    for m in mentors:
        db.execute(
            "INSERT INTO Mentors (fullname, profession, email, phone) "
            "VALUES (%s, %s, %s, %s)",
            m, commit=True,
        )
    print(f"Inserted {len(mentors)} mentors.")


def seed_assignments():
    """Create a few sponsor and mentor assignments.

    Pulls the actual generated IDs rather than assuming them, so this
    works regardless of auto-increment state.
    """
    students = db.fetch_all("SELECT student_id FROM Students ORDER BY student_id")
    sponsors = db.fetch_all("SELECT sponsor_id FROM Sponsors ORDER BY sponsor_id")
    mentors = db.fetch_all("SELECT mentor_id FROM Mentors ORDER BY mentor_id")

    # Assign the first two students a sponsor and a mentor each.
    if len(students) >= 2 and sponsors and mentors:
        db.execute(
            "INSERT INTO SponsorAssignments (sponsor_id, student_id, "
            "date_assigned) VALUES (%s, %s, %s)",
            (sponsors[0]["sponsor_id"], students[0]["student_id"], date.today()),
            commit=True,
        )
        db.execute(
            "INSERT INTO SponsorAssignments (sponsor_id, student_id, "
            "date_assigned) VALUES (%s, %s, %s)",
            (sponsors[1]["sponsor_id"], students[1]["student_id"], date.today()),
            commit=True,
        )
        db.execute(
            "INSERT INTO MentorAssignments (mentor_id, student_id, "
            "date_assigned) VALUES (%s, %s, %s)",
            (mentors[0]["mentor_id"], students[0]["student_id"], date.today()),
            commit=True,
        )
        print("Created sample sponsor and mentor assignments.")


def main():
    """Run the full seed process."""
    create_tables()
    clear_data()
    seed_students()
    seed_sponsors()
    seed_mentors()
    seed_assignments()
    print("\nSeed complete. The database is ready for demonstration.")
    db.close()


if __name__ == "__main__":
    main()