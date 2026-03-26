import sqlite3

def get_all_products():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    conn.close()
    return data

def get_product_by_id(pid):
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE product_id=?", (pid,))
    data = cursor.fetchall()
    conn.close()
    return data

def show_low_stock():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE quantity < 10")
    data = cursor.fetchall()
    conn.close()
    return data

def total_inventory_value():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(quantity * price) FROM products")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def display(data):
    print("\nProduct ID | Name | Category | Qty | Price")
    print("-" * 50)
    for row in data:
        print(row)

while True:
    print("\n--- Inventory System ---")
    print("1. View All Products")
    print("2. Search Product by ID")
    print("3. Show Low Stock")
    print("4. Total Inventory Value")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        display(get_all_products())

    elif choice == "2":
        pid = int(input("Enter Product ID: "))
        display(get_product_by_id(pid))

    elif choice == "3":
        display(show_low_stock())

    elif choice == "4":
        print("Total Value:", total_inventory_value())

    elif choice == "5":
        break

    else:
        print("Invalid choice")