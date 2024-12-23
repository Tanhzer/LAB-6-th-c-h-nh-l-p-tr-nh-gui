import tkinter as tk
from tkinter import messagebox
import sqlite3

# Kết nối với cơ sở dữ liệu SQLite
def connect_db():
    conn = sqlite3.connect('products.db')
    return conn

# Tạo bảng sản phẩm nếu chưa tồn tại
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Hàm thêm sản phẩm vào cơ sở dữ liệu
def add_product(name, price):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()

# Hàm tìm kiếm sản phẩm theo tên
def search_product(name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + name + '%',))
    products = cursor.fetchall()
    conn.close()
    return products

# Hàm cập nhật giá sản phẩm
def update_product(id, new_price):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET price = ? WHERE id = ?", (new_price, id))
    conn.commit()
    conn.close()

# Hàm xóa sản phẩm
def delete_product(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# Hàm cập nhật danh sách sản phẩm lên Listbox
def update_product_list():
    product_list.delete(0, tk.END)
    products = fetch_all_products()
    for product in products:
        product_list.insert(tk.END, f"ID: {product[0]} - Name: {product[1]} - Price: {product[2]}")

# Hàm lấy tất cả sản phẩm từ cơ sở dữ liệu
def fetch_all_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

# Hàm xử lý sự kiện thêm sản phẩm
def on_add_product():
    name = entry_name.get()
    try:
        price = float(entry_price.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid price.")
        return
    
    if name and price:
        add_product(name, price)
        update_product_list()
        entry_name.delete(0, tk.END)
        entry_price.delete(0, tk.END)
    else:
        messagebox.showerror("Input Error", "Please fill in both name and price.")

# Hàm xử lý sự kiện tìm kiếm sản phẩm
def on_search_product():
    name = entry_name.get()
    if name:
        products = search_product(name)
        product_list.delete(0, tk.END)
        for product in products:
            product_list.insert(tk.END, f"ID: {product[0]} - Name: {product[1]} - Price: {product[2]}")
    else:
        messagebox.showerror("Input Error", "Please enter a product name to search.")

# Hàm xử lý sự kiện cập nhật giá sản phẩm
def on_update_product():
    selected_product = product_list.curselection()
    if selected_product:
        product_id = int(product_list.get(selected_product[0]).split(" ")[1][:-1])
        try:
            new_price = float(entry_price.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid price.")
            return
        update_product(product_id, new_price)
        update_product_list()
        entry_price.delete(0, tk.END)
    else:
        messagebox.showerror("Selection Error", "Please select a product to update.")

# Hàm xử lý sự kiện xóa sản phẩm
def on_delete_product():
    selected_product = product_list.curselection()
    if selected_product:
        product_id = int(product_list.get(selected_product[0]).split(" ")[1][:-1])
        delete_product(product_id)
        update_product_list()
    else:
        messagebox.showerror("Selection Error", "Please select a product to delete.")

# Tạo cửa sổ GUI
root = tk.Tk()
root.title("Product Management")

# Tạo các widget
label_name = tk.Label(root, text="Product Name:")
label_name.grid(row=0, column=0)

entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

label_price = tk.Label(root, text="Product Price:")
label_price.grid(row=1, column=0)

entry_price = tk.Entry(root)
entry_price.grid(row=1, column=1)

add_button = tk.Button(root, text="Add Product", command=on_add_product)
add_button.grid(row=2, column=0, columnspan=2)

search_button = tk.Button(root, text="Search Product", command=on_search_product)
search_button.grid(row=3, column=0, columnspan=2)

update_button = tk.Button(root, text="Update Product Price", command=on_update_product)
update_button.grid(row=4, column=0, columnspan=2)

delete_button = tk.Button(root, text="Delete Product", command=on_delete_product)
delete_button.grid(row=5, column=0, columnspan=2)

product_list = tk.Listbox(root, width=50, height=10)
product_list.grid(row=6, column=0, columnspan=2)

# Tạo cơ sở dữ liệu và bảng nếu chưa có
create_table()

# Cập nhật danh sách sản phẩm khi khởi động
update_product_list()

# Chạy vòng lặp chính của ứng dụng GUI
root.mainloop()
