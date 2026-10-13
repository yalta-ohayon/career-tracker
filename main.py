from tracker import list_applications, list_by_status


def show_menu():
    """מדפיסה את התפריט"""
    print()
    print("=== Career Tracker ===")
    print("1. Add application")
    print("2. Update status")
    print("3. Show all applications")
    print("4. Show by status")
    print("0. Exit")

def print_applications(rows):
    """מדפיסה רשימת הגשות כטבלה מסודרת"""
    if not rows:
        print("No applications found.")
        return
    print(f"{'ID':<4}{'Company':<20}{'Position':<35}{'Date':<12}{'Status'}")
    print("-" * 80)
    for app_id, company, title, date, status in rows:
        print(f"{app_id:<4}{company:<20}{title:<35}{date:<12}{status}")


def main():
    """הלולאה הראשית של התוכנה"""
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("Coming soon...")
        elif choice == "2":
            print("Coming soon...")
        elif choice == "3":
            print_applications(list_applications())
        elif choice == "4":
            status = input("Enter status to filter by: ").strip()
            print_applications(list_by_status(status))        
        elif choice == "0":
            print("Good luck with your job search!")
            break     
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()