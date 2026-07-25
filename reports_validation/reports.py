#!/usr/bin/python3
import re
import mysql.connector


# reports.py - replace the connection function with this
import os

def get_database_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        port=int(os.environ.get('DB_PORT')),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME'),
        ssl_disabled=False
    )

    ──────────────────────────────────────
#  VALIDATION FUNCTIONS
# ─────────────────────────────────────────────

def validate_name(name):
    """
    Check that a name:
    - Is not empty
    - Contains only letters and spaces
    - Is at least 2 characters long
    Returns True if valid, False otherwise.
    """
    if not name or len(name.strip()) < 2:
        print("  [!] Name must be at least 2 characters long.")
        return False
    if not re.match(r"^[A-Za-z\s\-']+$", name.strip()):
        print("  [!] Name can only contain letters, spaces, hyphens, or apostrophes.")
        return False
    return True


def validate_email(email):
    """
    Check that an email address follows the standard format.
    Returns True if valid, False otherwise.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    if not email or not re.match(pattern, email.strip()):
        print("  [!] Invalid email address. Example: example@mail.com")
        return False
    return True


def validate_phone(phone):
    """
    Check that a phone number:
    - Contains only digits (and optional leading +)
    - Is between 10 and 15 characters
    Returns True if valid, False otherwise.
    """
    pattern = r'^\+?\d{10,15}$'
    if not phone or not re.match(pattern, phone.strip()):
        print("  [!] Invalid phone number. Must be 10-15 digits (e.g. 0241234567).")
        return False
    return True


def validate_menu_choice(choice, valid_options):
    """
    Check that the user's menu choice is in the list of valid options.
    Returns True if valid, False otherwise.
    """
    if choice not in valid_options:
        print(f"  [!] Invalid choice. Please select from: {', '.join(map(str, valid_options))}")
        return False
    return True


# ─────────────────────────────────────────────
#  COUNTING FUNCTIONS
# ─────────────────────────────────────────────

def count_students(cursor):
    """Return the total number of registered students."""
    cursor.execute("SELECT COUNT(*) FROM Students")
    return cursor.fetchone()[0]


def count_sponsored_students(cursor):
    """Return the number of students with an active sponsor."""
    cursor.execute(
        "SELECT COUNT(*) FROM Students WHERE sponsorship_status = 'sponsored'"
    )
    return cursor.fetchone()[0]


def count_unsponsored_students(cursor):
    """Return the number of students still waiting for a sponsor."""
    cursor.execute(
        "SELECT COUNT(*) FROM Students WHERE sponsorship_status = 'unsponsored'"
    )
    return cursor.fetchone()[0]


def count_sponsors(cursor):
    """Return the total number of registered sponsors."""
    cursor.execute("SELECT COUNT(*) FROM Sponsors")
    return cursor.fetchone()[0]


def count_mentors(cursor):
    """Return the total number of registered mentors."""
    cursor.execute("SELECT COUNT(*) FROM Mentors")
    return cursor.fetchone()[0]


def count_mentor_assignments(cursor):
    """Return the number of students who have been assigned a mentor."""
    cursor.execute(
        "SELECT COUNT(DISTINCT student_id) FROM Sponsorship_Records WHERE mentor_id IS NOT NULL"
    )
    return cursor.fetchone()[0]


# ─────────────────────────────────────────────
#  REPORT FUNCTION
# ─────────────────────────────────────────────

def generate_summary_report():
    """
    Connect to the database and print a full summary report
    covering students, sponsors, mentors, and assignments.
    """
    try:
        connection = get_database_connection()
        cursor = connection.cursor()

        total_students      = count_students(cursor)
        sponsored           = count_sponsored_students(cursor)
        unsponsored         = count_unsponsored_students(cursor)
        total_sponsors      = count_sponsors(cursor)
        total_mentors       = count_mentors(cursor)
        mentor_assignments  = count_mentor_assignments(cursor)

        # Calculate sponsorship percentage safely
        if total_students > 0:
            pct = round((sponsored / total_students) * 100, 1)
        else:
            pct = 0.0

        print("\n" + "=" * 50)
        print("   GIRLS EDUCATION PLATFORM – SUMMARY REPORT")
        print("=" * 50)

        print("\n📋 STUDENTS")
        print(f"   Total Registered     : {total_students}")
        print(f"   Sponsored            : {sponsored}")
        print(f"   Unsponsored          : {unsponsored}")
        print(f"   Sponsorship Rate     : {pct}%")

        print("\n💰 SPONSORS")
        print(f"   Total Registered     : {total_sponsors}")

        print("\n🎓 MENTORS")
        print(f"   Total Registered     : {total_mentors}")
        print(f"   Students with Mentor : {mentor_assignments}")

        print("\n" + "=" * 50)

        cursor.close()
        connection.close()

    except mysql.connector.Error as e:
        print(f"  [!] Database error: {e}")


# ─────────────────────────────────────────────
#  QUICK TEST (run this file directly to test)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("── Validation Tests ──────────────────────────")
    print(validate_name("Alice Mensah"))        # True
    print(validate_name("A"))                   # False – too short
    print(validate_name("Alice123"))            # False – has digits

    print(validate_email("alice@mail.com"))     # True
    print(validate_email("not-an-email"))       # False

    print(validate_phone("0241234567"))         # True
    print(validate_phone("123"))               # False – too short

    print(validate_menu_choice("1", ["1","2","3"]))   # True
    print(validate_menu_choice("9", ["1","2","3"]))   # False

    print("\n── Summary Report ────────────────────────────")
    generate_summary_report()
