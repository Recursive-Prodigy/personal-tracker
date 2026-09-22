from datetime import datetime
from database import list_books, delete_book, delete_books, update_book_field

def format_date_display(iso_date):
    return datetime.strptime(iso_date, "%Y-%m-%d").strftime("%d-%m-%Y")

def show_books():
    books = list_books()
    print("\nYour books:")
    for display_num, book in enumerate(books, start=1):
        book_id, title, author, price, date_purchased, category, format_ = book
        print(f"  {display_num}. [{book_id}] {title} — ₹{price} — {format_date_display(date_purchased)}")


def main():
    while True:
        show_books()
        print("\n1. Delete a book")
        print("2. Update a book info")
        print("3. Exit")
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
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()