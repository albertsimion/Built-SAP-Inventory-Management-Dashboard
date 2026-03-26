import streamlit as st
import sqlite3
import pandas as pd

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="Inventory Dashboard", page_icon="📦", layout="wide")

# ---------------- LOAD CSS ---------------- #
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------- DATABASE CONNECTION ---------------- #
def get_connection():
    return sqlite3.connect("products.db")

# ---------------- FUNCTIONS ---------------- #
def fetch_all_products():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return df

def search_product(product_id):
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM products WHERE product_id = ?",
        conn,
        params=(product_id,)
    )
    conn.close()
    return df

def low_stock_products():
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM products WHERE quantity < 10",
        conn
    )
    conn.close()
    return df

def total_inventory_value():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(quantity * price) FROM products")
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0

def total_products_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def low_stock_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products WHERE quantity < 10")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def add_product(pid, name, category, quantity, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (product_id, product_name, category, quantity, price) VALUES (?, ?, ?, ?, ?)",
        (pid, name, category, quantity, price)
    )
    conn.commit()
    conn.close()

def delete_product(pid):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = ?", (pid,))
    conn.commit()
    conn.close()

# ---------------- HEADER ---------------- #
st.title("📦Inventory Management Dashboard")
st.markdown("### Business Reporting Web App")

st.markdown("---")

# ---------------- DASHBOARD METRICS ---------------- #
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Products</div>
        <div class="metric-value">{total_products_count()}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Low Stock Items</div>
        <div class="metric-value">{low_stock_count()}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Inventory Value</div>
        <div class="metric-value">₹ {total_inventory_value():,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------- SIDEBAR ---------------- #
menu = st.sidebar.radio(
    "📌 Navigation",
    [
        "Dashboard",
        "Search Product",
        "Low Stock Report",
        "Add Product",
        "Delete Product"
    ]
)

# ---------------- DASHBOARD ---------------- #
if menu == "Dashboard":
    st.subheader("📋 Product Inventory Overview")
    df = fetch_all_products()
    st.dataframe(df, use_container_width=True)

# ---------------- SEARCH ---------------- #
elif menu == "Search Product":
    st.subheader("🔍 Search Product by ID")
    pid = st.number_input("Enter Product ID", min_value=1, step=1)

    if st.button("Search"):
        result = search_product(pid)
        if not result.empty:
            st.success("Product found successfully.")
            st.dataframe(result, use_container_width=True)
        else:
            st.error("No product found with that ID.")

# ---------------- LOW STOCK ---------------- #
elif menu == "Low Stock Report":
    st.subheader("⚠ Low Stock Products")
    low_stock = low_stock_products()

    if not low_stock.empty:
        st.warning("These products require restocking.")
        st.dataframe(low_stock, use_container_width=True)
    else:
        st.success("No low stock items found.")

# ---------------- ADD PRODUCT ---------------- #
elif menu == "Add Product":
    st.subheader("➕ Add New Product")

    col1, col2 = st.columns(2)

    with col1:
        pid = st.number_input("Product ID", min_value=1, step=1)
        name = st.text_input("Product Name")
        category = st.text_input("Category")

    with col2:
        quantity = st.number_input("Quantity", min_value=0, step=1)
        price = st.number_input("Price", min_value=0.0, step=1.0)

    if st.button("Add Product"):
        try:
            add_product(pid, name, category, quantity, price)
            st.success("Product added successfully.")
        except:
            st.error("Product ID already exists or invalid input.")

# ---------------- DELETE PRODUCT ---------------- #
elif menu == "Delete Product":
    st.subheader("🗑 Delete Product")

    pid = st.number_input("Enter Product ID to Delete", min_value=1, step=1)

    if st.button("Delete Product"):
        delete_product(pid)
        st.warning("Product deleted successfully.")