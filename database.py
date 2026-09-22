import sqlite3
from datetime import date

def list_books():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, author, price, date_purchased, category, format
        FROM book_purchases
        ORDER BY id
    """)
    rows = cursor.fetchall()

    conn.close()
    return rows


def delete_book(book_id):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM book_purchases WHERE id = ?", (book_id,))

    conn.commit()
    conn.close()

def delete_books(book_ids):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    placeholders = ",".join("?" for _ in book_ids)
    cursor.execute(f"DELETE FROM book_purchases WHERE id IN ({placeholders})", book_ids)

    conn.commit()
    conn.close()

def update_book_field(book_id, field, new_value):
    allowed_fields = {"title", "author", "price", "date_purchased", "category", "format"}

    if field not in allowed_fields:
        raise ValueError(f"Cannot update field: {field}")

    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    cursor.execute(f"UPDATE book_purchases SET {field} = ? WHERE id = ?", (new_value, book_id))

    conn.commit()
    conn.close()

def insert_entry(entry):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    entry_type = entry["type"]

    if entry_type == "book_purchase":

        if entry["date_purchased"] is None:
            entry["date_purchased"] = date.today().isoformat()

        cursor.execute("""
            INSERT INTO book_purchases
            (title, author, price, date_purchased, category, format)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entry["title"],
            entry["author"],
            entry["price"],
            entry["date_purchased"],
            entry["category"],
            entry["format"]
        ))

    elif entry_type == "buy_list":

        cursor.execute("""
            INSERT INTO buy_list
            (item, category, est_price, priority, status, date_added)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entry["item"],
            entry["category"],
            entry["est_price"],
            entry["priority"],
            entry["status"],
            entry["date_added"]
        ))

    elif entry_type == "build_list":

        cursor.execute("""
            INSERT INTO build_list
            (name, description, status, date_added, date_updated)
            VALUES (?, ?, ?, ?, ?)
        """, (
            entry["name"],
            entry["description"],
            entry["status"],
            entry["date_added"],
            entry["date_updated"]
        ))

    else:
        raise ValueError(f"Unknown entry type: {entry_type}")

    conn.commit()
    conn.close()

    return entry