"""Reports menu (integrates Member 6's reporting module)."""

from services.report_service import generate_summary_report
from utils.helpers import print_header, pause


def report_menu():
    """Display the platform summary report."""
    print_header("Platform Summary Report")
    stats = generate_summary_report()

    print("STUDENTS")
    print(f"   Total Registered     : {stats['total_students']}")
    print(f"   Sponsored            : {stats['sponsored']}")
    print(f"   Unsponsored          : {stats['unsponsored']}")
    print(f"   Sponsorship Rate     : {stats['sponsorship_rate']}%")

    print("\nSPONSORS")
    print(f"   Total Registered     : {stats['total_sponsors']}")

    print("\nMENTORS")
    print(f"   Total Registered     : {stats['total_mentors']}")
    print(f"   Students with Mentor : {stats['mentor_assignments']}")

    pause()