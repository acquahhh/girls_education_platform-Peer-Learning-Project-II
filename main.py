"""Girls Education Sponsorship & Mentorship Platform.

Application entry point. Initializes the database schema, then hands off
control to the main menu. Ensures the database connection is closed on
exit.
"""

from database.connection import db
from database.create_tables import create_tables
from menus.main_menu import MainMenu


def main():
    """Bootstrap and run the application."""
    try:
        # Ensure the schema exists before doing anything else.
        create_tables()
    except Exception as exc:  # noqa: BLE001 - fatal startup error
        print(f"Startup failed: {exc}")
        print("Check your Aiven credentials in the .env file and try "
              "again.")
        return

    try:
        MainMenu().run()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
    finally:
        db.close()


if __name__ == "__main__":
    main()