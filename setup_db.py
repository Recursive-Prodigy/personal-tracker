import sqlite3

conn = sqlite3.connect("tracker.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS book_purchases (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
author TEXT,
price REAL NOT NULL,
date_purchased TEXT NOT NULL,
category TEXT,
format TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS buy_list (
id INTEGER PRIMARY KEY AUTOINCREMENT,
item TEXT NOT NULL,
category TEXT,
est_price REAL,
priority TEXT,
status TEXT DEFAULT 'pending',
date_added TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS build_list (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
description TEXT,
status TEXT DEFAULT 'idea',
date_added TEXT NOT NULL,
date_updated TEXT
)
""")

conn.commit()
conn.close()

print("database created successfully with 3 tables twin!")