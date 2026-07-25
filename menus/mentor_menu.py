from utils.helpers import print_header, pause
import services.mentor_service as mentor_service


def ui_register_mentor():
    print_header("Register New Mentor")
    fullname = input("Enter Full Name: ").strip()
    profession = input("Enter Profession: ").strip()
    email = input("Enter Email Address: ").strip()
    phone = input("Enter Phone Number: ").strip()

    if not fullname or not email:
        print(" Error: Name and Email cannot be empty fields.")
        pause()
        return

    if mentor_service.register_mentor(fullname, profession, email, phone):
        print(" Mentor profile created successfully inside the database!")
    pause()


def ui_view_mentors():
    print_header("List of Active Mentors")
    mentors = mentor_service.get_all_mentors()
    if not mentors:
        print("No mentors found in the system database.")
        pause()
        return
    for m in mentors:
        print(
            f"ID: {m.mentor_id} | Name: {m.fullname} | Job: {m.profession} | Email: {m.email} | Phone: {m.phone}"
        )
    pause()


def ui_search_mentor():
    print_header("Search Mentor Records")
    term = input("Enter Mentor ID or Name to look up: ").strip()
    if not term:
        print(" Error: Search input cannot be empty.")
        pause()
        return

    results = mentor_service.search_mentors(term)
    if not results:
        print(" No matching mentor records found.")
        pause()
        return
    for m in results:
        print(
            f"Found -> ID: {m.mentor_id} | Name: {m.fullname} | Job: {m.profession} | Email: {m.email}"
        )
    pause()


def ui_update_mentor():
    print_header("Update Mentor Details")
    mentor_id = input("Enter Mentor ID to modify: ").strip()
    results = mentor_service.search_mentors(mentor_id)

    exact_match = None
    for m in results:
        if str(m.mentor_id) == mentor_id:
            exact_match = m
            break

    if not exact_match:
        print(" Error: Target Mentor ID not found.")
        pause()
        return

    print(
        f"Modifying record for {exact_match.fullname}. Leave empty to keep values."
    )
    fullname = (
        input(f"New Name [{exact_match.fullname}]: ").strip()
        or exact_match.fullname
    )
    profession = (
        input(f"New Profession [{exact_match.profession}]: ").strip()
        or exact_match.profession
    )
    email = (
        input(f"New Email [{exact_match.email}]: ").strip() or exact_match.email
    )
    phone = (
        input(f"New Phone [{exact_match.phone}]: ").strip() or exact_match.phone
    )

    if mentor_service.update_mentor_record(
        exact_match.mentor_id, fullname, profession, email, phone
    ):
        print(" Mentor profile updated successfully!")
    else:
        print("⚠️ Notice: No modifications were saved.")
    pause()


def ui_delete_mentor():
    print_header("Delete Mentor Record")
    mentor_id = input("Enter Mentor ID to remove: ").strip()
    confirm = (
        input(f"Are you sure you want to delete Mentor ID {mentor_id}? (yes/no): ")
        .strip()
        .lower()
    )

    if confirm == "yes":
        if mentor_service.delete_mentor_record(mentor_id):
            print(" Mentor record wiped from the database successfully.")
        else:
            print(" Failure: ID does not exist or database dropped query.")
    else:
        print("Operation cancelled.")
    pause()


def mentor_menu():
    while True:
        print_header("MENTOR MANAGEMENT MODULE")
        print("1. Register a New Mentor")
        print("2. Display All Mentors")
        print("3. Find a Mentor Record")
        print("4. Update Mentor Details")
        print("5. Delete a Mentor Profile")
        print("6. Return to Main Menu")

        choice = input("Select an alternative (1-6): ").strip()
        if choice == "1":
            ui_register_mentor()
        elif choice == "2":
            ui_view_mentors()
        elif choice == "3":
            ui_search_mentor()
        elif choice == "4":
            ui_update_mentor()
        elif choice == "5":
            ui_delete_mentor()
        elif choice == "6":
            print("Returning to application home screen hub...")
            break
        else:
            print("Choice Error: Enter a number from 1 to 6.")
            pause()

