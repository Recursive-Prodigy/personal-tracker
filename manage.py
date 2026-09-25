from datetime import datetime
from database import (
    list_books, delete_book, delete_books, delete_all_books, update_book_field,
    list_entries, delete_entries, delete_all_entries, update_entry_field
)


def format_date_display(iso_date):
    return datetime.strptime(iso_date, "%Y-%m-%d").strftime("%d-%m-%Y")


def show_books():
    books = list_books()
    print("\nYour books:")
    for display_num, book in enumerate(books, start=1):
        book_id, title, author, price, date_purchased, category, format_ = book
        print(f"  {display_num}. [{book_id}] {title} — ₹{price} — {format_date_display(date_purchased)}")


def manage_books():
    while True:
        show_books()
        print("\n1. Delete a book")
        print("2. Update a book info")
        print("3. Clear all books")
        print("4. Back")
        choice = input("Choose: ")

        if choice == "1":
            raw = input("Enter ID(s) to delete (comma-separated, e.g. 2,5,6) or press Enter to cancel: ")
            if raw.strip() == "":
                print("Cancelled.")
                continue
            try:
                book_ids = [int(x.strip()) for x in raw.split(",")]
            except ValueError:
                print("That's not valid, try again.")
                continue
            delete_books(book_ids)
            print(f"Deleted {len(book_ids)} book(s).")

        elif choice == "2":
            raw = input("Enter the ID to update (or press Enter to cancel): ")
            if raw.strip() == "":
                print("Cancelled.")
                continue
            try:
                book_id = int(raw)
            except ValueError:
                print("That's not a valid number, try again.")
                continue

            field = input("Which field? (title/author/price/date_purchased/category/format) or press Enter to cancel: ").strip()
            if field == "":
                print("Cancelled.")
                continue

            if field == "price":
                try:
                    new_value = float(input("New price: "))
                except ValueError:
                    print("Invalid price.")
                    continue
            else:
                new_value = input(f"New {field}: ").strip()

            try:
                update_book_field(book_id, field, new_value)
                print("Updated.")
            except ValueError as e:
                print(e)

        elif choice == "3":
            confirm = input("This will permanently delete ALL books, type 'yes' to confirm or press enter to cancel: ")
            if confirm.strip().lower() == "yes":
                delete_all_books()
                print("All books have been deleted.")
            else:
                print("Cancelled.")

        elif choice == "4":
            break

        else:
            print("Invalid choice.")


def show_table(table, label_fields):
    columns, rows = list_entries(table)
    print(f"\nYour {table}:")
    for i, row in enumerate(rows, start=1):
        row_dict = dict(zip(columns, row))
        summary = " — ".join(str(row_dict[f]) for f in label_fields)
        print(f"  {i}. [{row_dict['id']}] {summary}")


def manage_table(table, label_fields, allowed_fields):
    while True:
        show_table(table, label_fields)
        print("\n1. Delete entries")
        print("2. Update an entry")
        print("3. Clear all")
        print("4. Back")
        choice = input("Choose: ")

        if choice == "1":
            raw = input("Enter ID(s) to delete (comma-separated) or press Enter to cancel: ")
            if raw.strip() == "":
                print("Cancelled.")
                continue
            try:
                ids = [int(x.strip()) for x in raw.split(",")]
            except ValueError:
                print("That's not valid, try again.")
                continue
            delete_entries(table, ids)
            print(f"Deleted {len(ids)} entr{'y' if len(ids) == 1 else 'ies'}.")

        elif choice == "2":
            raw = input("Enter the ID to update (or press Enter to cancel): ")
            if raw.strip() == "":
                print("Cancelled.")
                continue
            try:
                entry_id = int(raw)
            except ValueError:
                print("Not a valid number.")
                continue

            field = input(f"Which field? ({'/'.join(allowed_fields)}) or press Enter to cancel: ").strip()
            if field == "":
                print("Cancelled.")
                continue

            new_value = input(f"New {field}: ").strip()

            try:
                update_entry_field(table, entry_id, field, new_value, allowed_fields)
                print("Updated.")
            except ValueError as e:
                print(e)

        elif choice == "3":
            confirm = input(f"This will permanently delete ALL {table} entries. Type 'yes' to confirm: ")
            if confirm.strip().lower() == "yes":
                delete_all_entries(table)
                print("Cleared.")
            else:
                print("Cancelled.")

        elif choice == "4":
            break

        else:
            print("Invalid choice.")


def main():
    while True:
        print("\n1. Manage books")
        print("2. Manage buy list")
        print("3. Manage build list")
        print("4. Exit")
        choice = input("Choose: ")

        if choice == "1":
            manage_books()
        elif choice == "2":
            manage_table("buy_list", label_fields=["item", "priority", "status"],
                          allowed_fields={"item", "category", "est_price", "priority", "status", "date_added"})
        elif choice == "3":
            manage_table("build_list", label_fields=["name", "status"],
                          allowed_fields={"name", "description", "status", "date_added", "date_updated"})
        elif choice == "4":
            print("Alright then have a great day/night ahead sire! Exiting now.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()