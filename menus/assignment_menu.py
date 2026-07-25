"""Assignment menu (Member 5).

Interactive CLI for matching sponsors and mentors to students. All
business logic lives in services/assignment_service.py - this module
only handles prompts, display, and routing.
"""

from services import assignment_service as svc
from utils.helpers import print_header, print_table, prompt, pause
from utils.validators import validate_positive_int


def assignment_menu():
    """Assignment menu loop."""
    while True:
        print_header("Assignments")
        print("1 Assign Sponsor to Student")
        print("2 Assign Mentor to Student")
        print("3 View Sponsorships")
        print("4 View Mentor Assignments")
        print("5 Remove Sponsorship")
        print("6 Remove Mentor Assignment")
        print("0 Back to Main Menu")
        choice = prompt("Select an option: ")

        try:
            if choice == "1":
                assign_sponsor()
            elif choice == "2":
                assign_mentor()
            elif choice == "3":
                view_sponsorships()
            elif choice == "4":
                view_mentor_assignments()
            elif choice == "5":
                remove_sponsorship()
            elif choice == "6":
                remove_mentor_assignment()
            elif choice == "0":
                return
            else:
                print("Invalid option. Please try again.")
        except ValueError as exc:
            print(f"\nError: {exc}")
            pause()
        except Exception as exc:  # noqa: BLE001 - surface errors to user
            print(f"\nAn unexpected error occurred: {exc}")
            pause()


def assign_sponsor():
    """Match a sponsor to a student."""
    students = svc.list_students()
    sponsors = svc.list_sponsors()

    if not students:
        print("\nNo students registered yet.")
        pause()
        return
    if not sponsors:
        print("\nNo sponsors registered yet.")
        pause()
        return

    print_header("Students")
    print_table(
        [{"id": s.student_id, "name": s.fullname, "school": s.school} for s in students],
        [("id", "ID"), ("name", "Name"), ("school", "School")],
    )
    student_id = validate_positive_int(prompt("\nEnter Student ID: "), "Student ID")

    print_header("Sponsors")
    print_table(
        [{"id": sp.sponsor_id, "name": sp.fullname, "org": sp.organization or "-"}
         for sp in sponsors],
        [("id", "ID"), ("name", "Name"), ("org", "Organization")],
    )
    sponsor_id = validate_positive_int(prompt("\nEnter Sponsor ID: "), "Sponsor ID")

    svc.create_sponsor_assignment(sponsor_id, student_id)
    print("\nSuccess! Sponsor assigned to student.")
    pause()


def assign_mentor():
    """Assign a mentor to a student."""
    students = svc.list_students()
    mentors = svc.list_mentors()

    if not students:
        print("\nNo students registered yet.")
        pause()
        return
    if not mentors:
        print("\nNo mentors registered yet.")
        pause()
        return

    print_header("Students")
    print_table(
        [{"id": s.student_id, "name": s.fullname, "school": s.school} for s in students],
        [("id", "ID"), ("name", "Name"), ("school", "School")],
    )
    student_id = validate_positive_int(prompt("\nEnter Student ID: "), "Student ID")

    print_header("Mentors")
    print_table(
        [{"id": m.mentor_id, "name": m.fullname, "profession": m.profession} for m in mentors],
        [("id", "ID"), ("name", "Name"), ("profession", "Profession")],
    )
    mentor_id = validate_positive_int(prompt("\nEnter Mentor ID: "), "Mentor ID")

    svc.create_mentor_assignment(mentor_id, student_id)
    print("\nSuccess! Mentor assigned to student.")
    pause()


def view_sponsorships():
    """Display every sponsorship on record."""
    print_header("All Sponsorships")
    rows = svc.list_sponsor_assignments()
    print_table(
        rows,
        [("assignment_id", "ID"), ("student_name", "Student"),
         ("sponsor_name", "Sponsor"), ("date_assigned", "Date Assigned")],
    )
    pause()


def view_mentor_assignments():
    """Display every mentor assignment on record."""
    print_header("All Mentor Assignments")
    rows = svc.list_mentor_assignments()
    print_table(
        rows,
        [("assignment_id", "ID"), ("student_name", "Student"),
         ("mentor_name", "Mentor"), ("date_assigned", "Date Assigned")],
    )
    pause()


def remove_sponsorship():
    """Remove a sponsorship by ID, after showing the current list."""
    rows = svc.list_sponsor_assignments()
    if not rows:
        print("\nNo sponsorships to remove.")
        pause()
        return

    print_header("Sponsorships")
    print_table(
        rows,
        [("assignment_id", "ID"), ("student_name", "Student"),
         ("sponsor_name", "Sponsor"), ("date_assigned", "Date Assigned")],
    )
    assignment_id = validate_positive_int(
        prompt("\nEnter the Sponsorship ID to remove: "), "Sponsorship ID"
    )
    svc.delete_sponsor_assignment(assignment_id)
    print("\nSponsorship removed.")
    pause()


def remove_mentor_assignment():
    """Remove a mentor assignment by ID, after showing the current list."""
    rows = svc.list_mentor_assignments()
    if not rows:
        print("\nNo mentor assignments to remove.")
        pause()
        return

    print_header("Mentor Assignments")
    print_table(
        rows,
        [("assignment_id", "ID"), ("student_name", "Student"),
         ("mentor_name", "Mentor"), ("date_assigned", "Date Assigned")],
    )
    assignment_id = validate_positive_int(
        prompt("\nEnter the Assignment ID to remove: "), "Assignment ID"
    )
    svc.delete_mentor_assignment(assignment_id)
    print("\nMentor assignment removed.")
    pause()
