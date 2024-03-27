import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pymongo import MongoClient
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


product_prices = {
    "Milk 1L": 60,
    "Coffee Powder 500g": 80,
    "Biscuits 1pc": 30,
    "Bread 1pc": 40,
    "Bun 1pc": 25,
    "Rice 1KG": 100,
    "Shampoo 100ML": 120,
    "Soap 1pc": 50,
    "Brush 1pc": 40,
    "Toothpaste 100gm": 35,
    "Ghee 1L": 150,
    "Butter 1pc": 70,
    "Buttermilk": 25,
    "Tomato 1KG": 20,
    "Onion 1KG": 15,
    "Potato 1KG": 45,  
    "Carrot 1KG": 30,
    "Beans 1KG": 35,
    "Beetroot 1KG": 40,
    "Cauliflower 1KG": 50,
    "Cabbage 1KG": 45,
    "Drumstick 1KG": 30,
    "Apple 1KG": 70,
    "Orange 1KG": 60,
    "Mango 1KG": 80,
    "Banana 1KG": 20,
    "Grapes 1KG": 100,
    "Watermelon 1KG": 40,
    "Papaya 1KG": 50,
    "Guava 1KG": 45,
    "Kiwi 1KG": 90,
    "Refined Oil 1L": 120,
    "Sunflower Oil 1L": 100,
    "Olive Oil 1L": 200,
    "Groundnut Oil 1L": 150,
    "Avocado Oil 1L": 180,
    "Pepsi 1L": 45,
    "Coca Cola 1L": 45,
    "Sprite 1L": 45,
    "Miranda 1L": 40,
    "Sting 1L": 50,
    "Bovonto 1L": 35,
    "Fruiti 1L": 30,
    "Slice 1L": 40,
    "Maaza 1L": 50,
    "Redbull 1L": 100,
    "Fizz 1L": 35,
    "Smoothie 1L": 60
}


client = MongoClient('mongodb://localhost:27017/')
db = client['invoice_database']
collection = db['invoices']

import os
def generate_pdf(data):
    folder_name = datetime.now().strftime('%Y-%m-%d')
    folder_path = os.path.join(os.getcwd(), "invoices", folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    file_name = f"Invoice_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    file_path = os.path.join(folder_path, file_name)
    
    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(100, 750, "ABC Store Invoice")
    c.drawString(100, 730, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 710, f"Customer: {data['customer_name']}")
    c.drawString(100, 690, f"Phone: {data['customer_phone']}")
    c.drawString(100, 670, "Products:")
    y = 650
    for product, details in data['products'].items():
        c.drawString(120, y, f"{product}: ₹ {details['price']} x {details['quantity']} = ₹ {details['total']}")
        y -= 20
    c.drawString(100, y - 30, f"Total: ₹ {data['total']}")
    c.save()

    return file_path

def save_to_mongodb():
    customer_name = customer_name_entry.get().strip()
    customer_phone = customer_phone_entry.get().strip()
    if not customer_name or not customer_phone:
        messagebox.showwarning("Warning", "Please enter customer name and phone number.")
        return

    data = {
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "date_time": datetime.now(),
        "products": products,
        "total": total_cost.get()
    }

    try:
        collection.insert_one(data)
        generate_pdf(data)
        messagebox.showinfo("Success", "Invoice saved and PDF generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def new_bill():
    customer_name_entry.delete(0, 'end')
    customer_phone_entry.delete(0, 'end')
    product_combobox.set('')
    category_combobox.set('')
    quantity_combobox.current(0)  
    product_combobox['values'] = []
    product_listbox.delete(*product_listbox.get_children())  
    total_cost.set(0)
    products.clear()


def update_product_dropdown(event):
    category = category_combobox.get()
    if category == 'Daily Essentials':
        products_list = ["Milk 1L", "Coffee Powder 500g", "Biscuits 1pc", "Bread 1pc", "Bun 1pc", "Rice 1KG", "Shampoo 100ML", "Soap 1pc", "Brush 1pc", "Toothpaste 100gm", "Ghee 1L", "Butter 1pc", "Buttermilk"]
    elif category == 'Vegetables':
        products_list = ["Tomato 1KG", "Onion 1KG", "Potato 1KG", "Carrot 1KG", "Beans 1KG", "Beetroot 1KG", "Cauliflower 1KG", "Cabbage 1KG", "Drumstick 1KG"]
    elif category == 'Fruits':
        products_list = ["Apple 1KG", "Orange 1KG", "Mango 1KG", "Banana 1KG", "Grapes 1KG", "Watermelon 1KG", "Papaya 1KG", "Guava 1KG", "Kiwi 1KG"]
    elif category == 'Oil':
        products_list = ["Refined Oil 1L", "Sunflower Oil 1L", "Olive Oil 1L", "Groundnut Oil 1L", "Avocado Oil 1L"]
    elif category == 'Beverages':
        products_list = ["Pepsi 1L", "Coca Cola 1L", "Sprite 1L", "Miranda 1L", "Sting 1L", "Bovonto 1L", "Fruiti 1L", "Slice 1L", "Maaza 1L", "Redbull 1L", "Fizz 1L", "Smoothie 1L"]
    else:
        products_list = []
    product_combobox['values'] = products_list

def popup_menu(event, listbox_widget):
    menu = tk.Menu(root, tearoff=0)

def delete_product():
    selected_item = product_listbox.focus()
    if selected_item:
        selected_item_values = product_listbox.item(selected_item)['values']
        selected_product_total = selected_item_values[3]
        product_listbox.delete(selected_item)
        selected_product_name = selected_item_values[0]
        products.pop(selected_product_name)
        update_total_cost()  

        messagebox.showinfo("Success", "Product removed successfully.")
        
def update_total_cost():
    total_cost.set(sum(detail['total'] for detail in products.values()))
def add_product():
    product = product_combobox.get().strip()
    quantity = quantity_combobox.get()
    if product:
        price = product_prices.get(product, 0)
        total_price = price * int(quantity)
        if product in products: 
            messagebox.showinfo("Product Already Selected", "This product is already added.")
        else:  
            products[product] = {'price': price, 'quantity': int(quantity), 'total': total_price}
            product_listbox.insert('', 'end', values=(product, price, quantity, total_price))
            update_total_cost()
def on_delete_key(event, listbox_widget):
    selection = listbox_widget.selection()
    if selection:
        delete_product(listbox_widget.index(selection[0]))

root = tk.Tk()
root.title("ABC INSTANT SHOPEE")
root.geometry("800x600")
root.configure(bg='#E6E6FA')

store_name_label = ttk.Label(root, text="ABC Store", font=('Helvetica', 24, 'bold'), background='#E6E6FA')
store_name_label.pack(pady=10)

customer_frame = ttk.Frame(root)
customer_frame.pack(padx=10, pady=10)

ttk.Label(customer_frame, text="Customer Name:").grid(row=0, column=0, padx=5, pady=5)
customer_name_entry = ttk.Entry(customer_frame)
customer_name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(customer_frame, text="Phone Number:").grid(row=1, column=0, padx=5, pady=5)
customer_phone_entry = ttk.Entry(customer_frame)
customer_phone_entry.grid(row=1, column=1, padx=5, pady=5)

product_frame = ttk.Frame(root)
product_frame.pack(padx=10, pady=10)

ttk.Label(product_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
category_combobox = ttk.Combobox(product_frame, values=["Daily Essentials", "Vegetables", "Fruits", "Oil", "Beverages"])
category_combobox.grid(row=0, column=1, padx=5, pady=5)
category_combobox.bind("<<ComboboxSelected>>", update_product_dropdown)

ttk.Label(product_frame, text="Product:").grid(row=0, column=2, padx=5, pady=5)
product_combobox = ttk.Combobox(product_frame)
product_combobox.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(product_frame, text="Quantity:").grid(row=0, column=4, padx=5, pady=5)
quantity_combobox = ttk.Combobox(product_frame, values=[str(i) for i in range(1, 11)])  # Scale from 1 to 10
quantity_combobox.grid(row=0, column=5, padx=5, pady=5)
quantity_combobox.current(0)

add_button = ttk.Button(product_frame, text="Add Product", command=add_product)
add_button.grid(row=0, column=6, padx=5, pady=5)

product_listbox = ttk.Treeview(root, columns=('Product', 'Price', 'Quantity', 'Total Price'))
product_listbox.pack(padx=10, pady=10)
product_listbox.heading('Product', text='Product')
product_listbox.heading('Price', text='Price')
product_listbox.heading('Quantity', text='Quantity')
product_listbox.heading('Total Price', text='Total Price')

total_cost = tk.IntVar()
ttk.Label(root, text="Total Cost:").pack(pady=5)
tk.Entry(root, textvariable=total_cost, state='readonly', font=("Helvetica", 12)).pack(pady=5)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

save_button = ttk.Button(button_frame, text="Save", command=save_to_mongodb)
save_button.grid(row=0, column=0, padx=5)

new_bill_button = ttk.Button(button_frame, text="New Bill", command=new_bill)
new_bill_button.grid(row=0, column=1, padx=5)

product_listbox.bind("<Delete>", lambda e: (delete_product(), 'break'))


contact_label = ttk.Label(root, text="Contact us:\n naveenwilson12@gmail.com\nto make any update in the software", background='#E6E6FA')
contact_label.pack(side="bottom", pady=10)

products = {}

root.mainloop()

