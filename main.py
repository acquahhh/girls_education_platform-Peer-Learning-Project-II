"""Girls Education Sponsorship & Mentorship Platform.

Application entry point (Member 1 - Integration Lead). Initializes the
database schema, then launches the main menu. Ensures the database
connection is closed on exit.
"""

from database.connection import db
from database.create_tables import create_tables
from menus.main_menu import run_application


def main():
    """Bootstrap and run the application."""
    try:
        create_tables()
    except Exception as exc:  # noqa: BLE001 - fatal startup error
        print(f"Startup failed: {exc}")
        print("Check your Aiven credentials in the .env file and try "
              "again.")
        return

    try:
        run_application()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
    finally:
        db.close()


if __name__ == "__main__":
    main()