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

def spending_by_year():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT strftime('%Y', date_purchased) AS year, SUM(price), COUNT(*)
        FROM book_purchases
        GROUP BY year
        ORDER BY year
    """)
    results = cursor.fetchall()

    conn.close()
    return results


def spending_by_month():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT strftime('%Y-%m', date_purchased) AS year_month, SUM(price), COUNT(*)
        FROM book_purchases
        GROUP BY year_month
        ORDER BY year_month
    """)
    results = cursor.fetchall()

    conn.close()
    return results

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

    print("\nSpending by year:")
    for year, spent, num_books in spending_by_year():
        print(f"  {year}: ₹{spent} ({num_books} book{'s' if num_books != 1 else ''})")

    print("\nSpending by month:")
    for year_month, spent, num_books in spending_by_month():
        print(f"  {year_month}: ₹{spent} ({num_books} book{'s' if num_books != 1 else ''})")