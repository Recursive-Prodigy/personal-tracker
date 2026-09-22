import sqlite3
import requests

def get_inr_to_usd_rate():
    try:
         url="https://open.er-api.com/v6/latest/INR"
         response= requests.get(url)
         data= response.json()
         return data["rates"]["USD"]
    except requests.exceptions.RequestException:
        return None

def get_total_book_spending():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(price)
        FROM book_purchases
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total or 0

def get_book_count():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM book_purchases")
    count = cursor.fetchone()[0]

    conn.close()

    return count

if __name__ == "__main__":
    total = get_total_book_spending()
    count = get_book_count()

    usd_rate= get_inr_to_usd_rate()

    if usd_rate:
         total_usd= total*usd_rate
         print(f"Total spent on books: {total} or (${total_usd:.2f})")
    else:
        print(f"Total spent on books: {total} (USD unavailable without internet)")

    print(f"Books purchased: {count}")