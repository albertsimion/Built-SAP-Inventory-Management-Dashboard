import sqlite3

conn = sqlite3.connect("products.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
""")

sample_data = [
    (101, "Mouse", "Electronics", 25, 500),
    (102, "Keyboard", "Electronics", 8, 1200),
    (103, "Notebook", "Stationery", 50, 80),
    (104, "Pen", "Stationery", 5, 20),
    (105, "Monitor", "Electronics", 12, 9500),
    (106, "USB Cable", "Electronics", 6, 250),
    (107, "Marker", "Stationery", 15, 60)
]

for item in sample_data:
    cursor.execute("INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?, ?)", item)

conn.commit()
conn.close()

print("Database setup complete!")