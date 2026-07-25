"""Main menu and application flow (Member 1 - Integration Lead).

Displays the top-level menu and routes to each teammate's module.
Contains no business logic itself; it delegates to the menu modules
owned by Members 2-6.
"""

from menus.student_menu import student_menu
from menus.sponsor_menu import sponsor_menu
from menus.mentor_menu import mentor_menu
from menus.assignment_menu import assignment_menu
from menus.report_menu import report_menu
from utils.helpers import print_header, prompt


def display_main_menu():
    """Print the main menu options."""
    print_header("Girls Education Platform")
    print("1 Manage Students")
    print("2 Manage Sponsors")
    print("3 Manage Mentors")
    print("4 Assignments")
    print("5 Reports")
    print("0 Exit")


def run_application():
    """Run the main application loop until the user exits."""
    while True:
        display_main_menu()
        choice = prompt("Select an option: ")

        try:
            if choice == "1":
                student_menu()
            elif choice == "2":
                sponsor_menu()
            elif choice == "3":
                mentor_menu()
            elif choice == "4":
                assignment_menu()
            elif choice == "5":
                report_menu()
            elif choice == "0":
                print("\nGoodbye.")
                return
            else:
                print("Invalid option. Please try again.")
        except Exception as exc:  # noqa: BLE001 - surface errors to user
            print(f"An error occurred: {exc}")