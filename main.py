from datetime import date

from database import init_db
from tracker import (STATUSES, list_applications, list_by_status, update_status,
                     find_or_add_company, add_position, add_application,
                     count_by_status, stats_by_company, response_rate)


def show_menu():
    """Print the main menu."""
    print()
    print("=== Career Tracker ===")
    print("1. Add application")
    print("2. Update status")
    print("3. Show all applications")
    print("4. Show by status")
    print("5. Statistics")
    print("0. Exit")


def print_applications(rows):
    """Print a list of applications as an aligned table."""
    if not rows:
        print("No applications found.")
        return
    print(f"{'ID':<4}{'Company':<20}{'Position':<35}{'Date':<12}{'Status'}")
    print("-" * 80)
    for app_id, company, title, applied, status in rows:
        print(f"{app_id:<4}{company[:19]:<20}{title[:34]:<35}{applied:<12}{status}")


def ask(prompt, required=True):
    """Ask for input; repeat until something is typed if the field is required."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value or None
        print("This field is required.")


def ask_date(prompt):
    """Ask for a date in YYYY-MM-DD format. Empty input means today."""
    while True:
        value = input(prompt).strip()
        if not value:
            return str(date.today())
        try:
            date.fromisoformat(value)
            return value
        except ValueError:
            print("Please use the format YYYY-MM-DD, for example 2026-10-20.")


def ask_status():
    """Ask the user to pick one of the allowed statuses by number."""
    for i, status in enumerate(STATUSES, start=1):
        print(f"  {i}. {status}")
    while True:
        choice = input("Choose status number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(STATUSES):
            return STATUSES[int(choice) - 1]
        print("Invalid choice, please try again.")


def add_application_flow():
    """Collect application details from the user and save them."""
    company = ask("Company name: ")
    field = ask("Company field (optional): ", required=False)
    title = ask("Position title: ")
    applied = ask_date("Date applied (YYYY-MM-DD, empty = today): ")
    notes = ask("Notes (optional): ", required=False)

    company_id = find_or_add_company(company, field)
    position_id = add_position(title, company_id)
    app_id = add_application(position_id, applied, notes)
    print(f"Application #{app_id} added!")


def update_status_flow():
    """Let the user change the status of an existing application."""
    print_applications(list_applications())
    app_id = ask("Application ID to update: ")
    if not app_id.isdigit():
        print("ID must be a number.")
        return
    new_status = ask_status()
    note = ask("Add a note (optional): ", required=False)
    if update_status(int(app_id), new_status, note):
        print(f"Application #{app_id} is now '{new_status}'.")
    else:
        print(f"No application with ID {app_id}.")


def show_by_status_flow():
    """Show only the applications with a chosen status."""
    print_applications(list_by_status(ask_status()))


def show_statistics():
    """Print a summary report of all applications."""
    total, answered, percent = response_rate()
    if total == 0:
        print("No applications yet.")
        return
    print(f"\nTotal applications: {total}")
    print(f"Got a reply: {answered} ({percent}%)")

    print("\nBy status:")
    for status, count in count_by_status():
        print(f"  {status:<12}{count:>3}  {'#' * count}")

    print("\nBy company:")
    print(f"  {'Company':<20}{'Total':>6}{'Rejected':>10}{'Waiting':>9}{'Progressed':>12}")
    for name, company_total, rejected, waiting, progressed in stats_by_company():
        print(f"  {name[:19]:<20}{company_total:>6}{rejected:>10}{waiting:>9}{progressed:>12}")


def main():
    """Main program loop."""
    init_db()
    actions = {
        "1": add_application_flow,
        "2": update_status_flow,
        "3": lambda: print_applications(list_applications()),
        "4": show_by_status_flow,
        "5": show_statistics,
    }
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Good luck with your job search!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()