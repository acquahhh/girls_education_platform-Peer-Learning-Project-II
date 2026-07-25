"""Sponsor management menu."""

from utils.helpers import print_header, pause
from utils.validators import validate_email, validate_phone
import services.sponsor_service as sponsor_service


def ui_register_sponsor():
    print_header("Register New Sponsor")
    fullname = input("Full Name: ").strip()
    organization = input("Organization: ").strip()
    email = input("Email Address: ").strip()
    phone = input("Phone Number: ").strip()

    if not fullname or not email:
        print("[!] Error: Name and Email cannot be empty.")
        pause()
        return

    try:
        email = validate_email(email)
        phone = validate_phone(phone)
    except ValueError as exc:
        print(f"[!] {exc}")
        pause()
        return

    organization = organization or None

    if sponsor_service.register_sponsor(fullname, organization, email, phone):
        print("Sponsor registered successfully.")
    pause()


def ui_view_sponsors():
    print_header("All Sponsors")
    sponsors = sponsor_service.get_all_sponsors()
    if not sponsors:
        print("No sponsors found in the database.")
        pause()
        return
    for s in sponsors:
        print(
            f"ID: {s.sponsor_id} | Name: {s.fullname} | Org: {s.organization or '-'} | Email: {s.email} | Phone: {s.phone}"
        )
    pause()


def ui_search_sponsor():
    print_header("Search Sponsor Records")
    term = input("Enter Sponsor ID or Name: ").strip()
    if not term:
        print("[!] Error: Search input cannot be empty.")
        pause()
        return

    results = sponsor_service.search_sponsors(term)
    if not results:
        print("[!] No matching sponsor records found.")
        pause()
        return
    for s in results:
        print(
            f"Found -> ID: {s.sponsor_id} | Name: {s.fullname} | Org: {s.organization or '-'} | Email: {s.email}"
        )
    pause()


def ui_update_sponsor():
    print_header("Update Sponsor Details")
    sponsor_id = input("Enter Sponsor ID to modify: ").strip()
    results = sponsor_service.search_sponsors(sponsor_id)

    exact_match = None
    for s in results:
        if str(s.sponsor_id) == sponsor_id:
            exact_match = s
            break

    if not exact_match:
        print("[!] Error: Target Sponsor ID not found.")
        pause()
        return

    print(f"Modifying record for {exact_match.fullname}. Leave empty to keep values.")
    fullname = input(f"New Name [{exact_match.fullname}]: ").strip() or exact_match.fullname
    organization = input(f"New Organization [{exact_match.organization or '-'}]: ").strip() or exact_match.organization
    email = input(f"New Email [{exact_match.email}]: ").strip() or exact_match.email
    phone = input(f"New Phone [{exact_match.phone}]: ").strip() or exact_match.phone

    try:
        email = validate_email(email)
        phone = validate_phone(phone)
    except ValueError as exc:
        print(f"[!] {exc}")
        pause()
        return

    if sponsor_service.update_sponsor_record(
        exact_match.sponsor_id, fullname, organization, email, phone
    ):
        print("Sponsor updated successfully.")
    else:
        print("[!] Notice: No modifications were saved.")
    pause()


def ui_delete_sponsor():
    print_header("Delete Sponsor Record")
    sponsor_id = input("Enter Sponsor ID to remove: ").strip()

    results = sponsor_service.search_sponsors(sponsor_id)
    match = None
    for s in results:
        if str(s.sponsor_id) == sponsor_id:
            match = s
            break

    if not match:
        print("[!] Error: Sponsor ID not found.")
        pause()
        return

    print(f"Found: {match.fullname} | Org: {match.organization or '-'} | Email: {match.email}")
    confirm = input(f"Delete this sponsor (ID {sponsor_id})? (yes/no): ").strip().lower()

    if confirm == "yes":
        if sponsor_service.delete_sponsor_record(sponsor_id):
            print("Sponsor record deleted successfully.")
        else:
            print("[!] Failure: could not delete.")
    else:
        print("[!] Operation cancelled.")
    pause()


def sponsor_menu():
    while True:
        print_header("SPONSOR MANAGEMENT MODULE")
        print("1. Register a New Sponsor")
        print("2. Display All Sponsors")
        print("3. Find a Sponsor Record")
        print("4. Update Sponsor Details")
        print("5. Delete a Sponsor Profile")
        print("6. Return to Main Menu")

        choice = input("Select an option (1-6): ").strip()
        if choice == "1":
            ui_register_sponsor()
        elif choice == "2":
            ui_view_sponsors()
        elif choice == "3":
            ui_search_sponsor()
        elif choice == "4":
            ui_update_sponsor()
        elif choice == "5":
            ui_delete_sponsor()
        elif choice == "6":
            break
        else:
            print("[!] Invalid choice. Enter a number from 1 to 6.")
            pause()