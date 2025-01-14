import tkinter as tk
from tkinter import messagebox, scrolledtext
# from inventory.product import Product
# from inventory.category import Category
from inventory.inventory_manager import InventoryManager
from data_handler import DataHandler
# from datetime import datetime
# import os
# import json
from PIL import Image, ImageTk  # Import Pillow to handle more image formats

# Define file name for JSON storage
DATA_FILE = "inventory/data.json"

# Load data
data = DataHandler.load_from_json_file(DATA_FILE)

# Initialize inventory manager
inventory = InventoryManager()
inventory.load_data_from_json(data)


def save():
    try:
        exported_data = inventory.export_to_json()
    except TypeError as e:
        print("Serialization error:", e)
    DataHandler.save_to_json_file(exported_data, DATA_FILE)


# Function to display output in a styled text widget
def display_output(text):
    output_box.config(state=tk.NORMAL)  # Enable editing
    output_box.delete(1.0, tk.END)  # Clear previous text
    output_box.insert(tk.END, text)  # Insert new text
    output_box.config(state=tk.DISABLED)  # Disable editing


# Function to show all products
def show_products():
    output_text = "\nAll Products in Inventory:\n"
    for product_id in inventory.get_products():
        product_info = inventory.get_product_info_by_id(product_id)
        output_text += f"{product_info}\n{'-'*40}\n"
    display_output(output_text)


# Function to show all categories
def show_categories():
    output_text = "\nCategories:\n"
    for category in inventory.get_categories().values():
        output_text += (
            f"ID: {category.id}, Category: {category.name}\n{'-'*40}\n"
        )
    display_output(output_text)


# Function to show products by categories
def show_products_by_category():
    def submit_category_id():
        try:
            category_id = int(entry_category_id.get())
            if category_id in range(0, inventory.get_max_category_id() + 1):
                products_by_category = inventory.get_products_by_category(
                    category_id
                    )
                output_text = f"\nProducts in Category ID {category_id}:\n"
                for product in products_by_category:
                    output_text += f"{product}\n"
                display_output(output_text)
                new_category_window.destroy()
            else:
                messagebox.showwarning(
                    "Invalid Category ID",
                    "The entered category ID is not valid."
                    )
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    # New window for category ID input
    new_category_window = tk.Toplevel(window)
    new_category_window.title("Enter Category ID")
    new_category_window.geometry("400x200")

    tk.Label(new_category_window, text="Enter category ID:").pack(pady=10)
    entry_category_id = tk.Entry(new_category_window)
    entry_category_id.pack(pady=10)

    submit_button = tk.Button(
        new_category_window,
        text="Show Products by Category ID",
        command=submit_category_id
        )
    submit_button.pack(pady=10)


# Function to search for products
def search_product():
    def submit_search():
        search_term = str(entry_search.get())
        if search_term:
            try:
                search_results = inventory.search_product(search_term)
                output_text = f"Product Info for '{search_term}':\n"
                if isinstance(search_results, list):
                    for result in search_results:
                        output_text += f"{result}\n{'-'*40}\n"
                else:
                    output_text += f"{search_results}\n{'-'*40}\n"
                display_output(output_text)
            except ValueError as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showwarning(
                "Input Error", "Please enter a product name."
                )

    new_window = tk.Toplevel(window)
    new_window.title("Product Search")
    new_window.geometry("400x200")

    tk.Label(new_window, text="Enter product name:").pack(pady=10)
    entry_search = tk.Entry(new_window)
    entry_search.pack(pady=10)
    submit_button = tk.Button(new_window, text="Search", command=submit_search)
    submit_button.pack(pady=10)


# Function to add new product
def add_product():
    def submit_product():
        try:
            details = entry_add_product.get().split(",")
            if len(details) == 4:
                product_name, price, quantity, category_id = details
                new_product = {
                    "name": product_name,
                    "price": float(price),
                    "quantity": int(quantity),
                    "category": int(category_id)
                    }
                inventory.add_product(new_product)
                messagebox.showinfo(
                    "Success", f"Product '{product_name}' added successfully."
                    )
                save()
                new_window.destroy()
            else:
                messagebox.showwarning(
                    "Input Error",
                    "Please provide product details in the format: "
                    "name, price, quantity, category_id."
                    )
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    new_window = tk.Toplevel(window)
    new_window.title("Add New Product")
    new_window.geometry("400x200")

    tk.Label(
        new_window,
        text="Enter product details (name, price, quantity, category_id):"
        ).pack(pady=10)
    entry_add_product = tk.Entry(new_window)
    entry_add_product.pack(pady=10)
    submit_button = tk.Button(
        new_window,
        text="Add Product",
        command=submit_product
        )
    submit_button.pack(pady=10)


# Function to add new category
def add_category():
    def submit_category():
        category_name = entry_add_category.get()
        if category_name:
            try:
                inventory.add_category(category_name)
                messagebox.showinfo(
                    "Success",
                    f"Category '{category_name}' added successfully."
                    )
                save()
                new_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showwarning(
                "Input Error", "Please enter a category name."
                )

    new_window = tk.Toplevel(window)
    new_window.title("Add New Category")
    new_window.geometry("400x200")

    tk.Label(new_window, text="Enter category name:").pack(pady=10)
    entry_add_category = tk.Entry(new_window)
    entry_add_category.pack(pady=10)
    submit_button = tk.Button(
        new_window,
        text="Add Category",
        command=submit_category
        )
    submit_button.pack(pady=10)


# Function to update product details
def update_product():
    def submit_update():
        try:
            product_id = entry_product_id.get()
            new_value = entry_new_value.get()

            if not product_id or not new_value:
                messagebox.showwarning(
                    "Input Error",
                    "Please provide both product ID and new value."
                    )
                return

            if choice.get() == 1:  # Update product name
                inventory.update_product_name(int(product_id), str(new_value))
                messagebox.showinfo(
                    "Success",
                    f"Product {product_id} name updated to '{new_value}'."
                    )
            elif choice.get() == 2:  # Update product price
                inventory.update_product_price(
                    int(product_id), float(new_value)
                    )
                messagebox.showinfo(
                    "Success",
                    f"Product {product_id} price updated to {new_value}."
                    )
            elif choice.get() == 3:  # Update product quantity
                inventory.update_product_quantity(
                    int(product_id), int(new_value)
                    )
                messagebox.showinfo(
                    "Success",
                    f"Product {product_id} quantity updated to {new_value}."
                    )
            elif choice.get() == 4:  # Update category
                inventory.update_product_category(
                    int(product_id), int(new_value)
                    )
                messagebox.showinfo(
                    "Success",
                    f"Product {product_id} category updated to '{new_value}'."
                    )
            else:
                messagebox.showwarning(
                    "Input Error",
                    "Please select a valid update option."
                    )
            save()
            new_window.destroy()  # Close the update window after submission
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    # Create a new window for updating product details
    new_window = tk.Toplevel(window)
    new_window.title("Update Product Details")
    new_window.geometry("500x400")

    # Radio buttons for selecting the update option
    choice_label = tk.Label(new_window, text="What would you like to update?")
    choice_label.pack(pady=10)

    choice = tk.IntVar()
    choice.set(1)  # Default is updating product name
    tk.Radiobutton(
        new_window, text="Product Name", variable=choice, value=1
        ).pack()
    tk.Radiobutton(
        new_window, text="Product Price", variable=choice, value=2
        ).pack()
    tk.Radiobutton(
        new_window, text="Product Quantity", variable=choice, value=3
        ).pack()
    tk.Radiobutton(
        new_window, text="Product Category", variable=choice, value=4
        ).pack()

    # Entry fields for product ID and new value
    entry_product_id_label = tk.Label(new_window, text="Enter Product ID:")
    entry_product_id_label.pack(pady=5)
    entry_product_id = tk.Entry(new_window)
    entry_product_id.pack(pady=5)

    entry_new_value_label = tk.Label(new_window, text="Enter new value:")
    entry_new_value_label.pack(pady=5)
    entry_new_value = tk.Entry(new_window)
    entry_new_value.pack(pady=5)

    # Submit button
    submit_button = tk.Button(
        new_window,
        text="Submit Update",
        command=submit_update
        )
    submit_button.pack(pady=10)


# Function to remove product or category
def remove_item():
    def submit_removal():
        try:
            choice = var_choice.get()
            if choice == 1:  # Remove Product
                product_id = entry_id.get()
                if product_id:
                    product_id = int(product_id)
                    inventory.remove_product(product_id)
                    messagebox.showinfo(
                        "Success",
                        f"Product with ID {product_id} removed successfully."
                        )
                else:
                    messagebox.showwarning(
                        "Input Error",
                        "Please enter a valid product ID."
                        )

            elif choice == 2:  # Remove Category
                category_id = entry_id.get()
                if category_id:
                    category_id = int(category_id)
                    inventory.remove_category(category_id)
                    messagebox.showinfo(
                        "Success", f"Category with ID {category_id}"
                        " removed successfully."
                        )
                else:
                    messagebox.showwarning
                    ("Input Error",
                     "Please enter a valid category ID."
                     )
            else:
                messagebox.showwarning(
                    "Choice Error",
                    "Please select either Product or Category to remove."
                    )
            save()
            new_window.destroy()  # Close the removal window after submission
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    # Create a new window for removing product or category
    new_window = tk.Toplevel(window)
    new_window.title("Remove Item")
    new_window.geometry("400x300")

    # Radio buttons for selecting product or category removal
    var_choice = tk.IntVar()
    var_choice.set(1)  # Default to remove product
    choice_label = tk.Label(new_window, text="What would you like to remove?")
    choice_label.pack(pady=10)

    tk.Radiobutton(
        new_window, text="Product", variable=var_choice, value=1
        ).pack()
    tk.Radiobutton(
        new_window, text="Category", variable=var_choice, value=2
        ).pack()

    # Entry field for ID input
    entry_id_label = tk.Label(
        new_window, text="Enter the ID of the item to remove:"
        )
    entry_id_label.pack(pady=5)
    entry_id = tk.Entry(new_window)
    entry_id.pack(pady=5)

    # Submit button
    submit_button = tk.Button(
        new_window,
        text="Submit Removal",
        command=submit_removal
        )
    submit_button.pack(pady=10)


def show_inventory_value_options():
    def show_total_value():
        total_value = inventory.get_total_inventory_value()
        output_text = (
            f"\nTotal Inventory Value for All Products: €"
            f"{total_value:.2f}\n"
        )
        display_output(output_text)
        new_window.destroy()

    def show_value_by_category():
        def submit_category_id():
            try:
                category_id = int(entry_category_id.get())
                if category_id in range(
                    0, inventory.get_max_category_id() + 1
                ):
                    total_value = (
                        inventory.get_total_inventory_value_by_category(
                            category_id
                            )
                    )
                    output_text = (
                        f"\nTotal Inventory Value for Category ID"
                        f"{category_id}: €{total_value:.2f}\n"
                    )
                    display_output(output_text)
                    new_category_window.destroy()
                else:
                    messagebox.showwarning(
                        "Invalid Input", "Category ID is not valid."
                        )
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")

        # New window to enter category ID
        new_category_window = tk.Toplevel(window)
        new_category_window.title("Enter Category ID")
        new_category_window.geometry("400x200")

        tk.Label(new_category_window, text="Enter category ID:").pack(pady=10)
        entry_category_id = tk.Entry(new_category_window)
        entry_category_id.pack(pady=10)

        submit_button = tk.Button(
            new_category_window,
            text="Get Value by Category",
            command=submit_category_id
            )
        submit_button.pack(pady=10)

    # Create a new window with options to choose
    new_window = tk.Toplevel(window)
    new_window.title("Total Inventory Value Options")
    new_window.geometry("400x200")

    # Add buttons for both options
    btn_total_value = tk.Button(
        new_window,
        text="Total Inventory Value (All Products)",
        command=show_total_value
        )
    btn_total_value.pack(pady=10)

    btn_value_by_category = tk.Button(
        new_window,
        text="Total Value by Category",
        command=show_value_by_category
        )
    btn_value_by_category.pack(pady=10)


# Initialize the main window
window = tk.Tk()
window.title("Inventory Management")
# Get the screen's width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window to cover the full screen
window.geometry(f"{screen_width}x{screen_height}")
window.config(bg="black")

# Load and set the background image
image = Image.open("inv5.png")  # Load the image
image = image.resize((screen_width, screen_height))  # Resize to screen size
background_image = ImageTk.PhotoImage(image)

# Create a label to hold the background image
background_label = tk.Label(window, image=background_image)
background_label.place(relwidth=1, relheight=1)  # It covers the full window

# Create a frame for buttons
button_frame = tk.Frame(window, bg="blue")
button_frame.pack(fill=tk.X, pady=10)

# Add buttons for menu options
btn_show_products = tk.Button(
    button_frame,
    text="Show Products",
    command=show_products,
    width=20
)
btn_show_products.pack(side=tk.LEFT, padx=5)

btn_show_categories = tk.Button(
    button_frame,
    text="Show Categories",
    command=show_categories,
    width=20
)
btn_show_categories.pack(side=tk.LEFT, padx=5)

# Add a new button for showing products by category
btn_show_products_by_category = tk.Button(
    button_frame,
    text="Show Products by Category",
    command=show_products_by_category,
    width=30
)
btn_show_products_by_category.pack(side=tk.LEFT, padx=5)

btn_search_product = tk.Button(
    button_frame,
    text="Search Product",
    command=search_product,
    width=20
)
btn_search_product.pack(side=tk.LEFT, padx=5)

btn_add_product = tk.Button(
    button_frame,
    text="Add Product",
    command=add_product,
    width=20
)
btn_add_product.pack(side=tk.LEFT, padx=5)

btn_add_category = tk.Button(
    button_frame,
    text="Add Category",
    command=add_category,
    width=20
)
btn_add_category.pack(side=tk.LEFT, padx=5)

# Add the "Update Product" button to the main window
btn_update_product = tk.Button(
    button_frame,
    text="Update Product",
    command=update_product,
    width=20
)
btn_update_product.pack(side=tk.LEFT, padx=5)

# Add the "Remove Product/Category" button to the main window
btn_remove_item = tk.Button(
    button_frame,
    text="Remove Product/Category",
    command=remove_item,
    width=20
)
btn_remove_item.pack(side=tk.LEFT, padx=5)

# Add a new button for Total Inventory Value options
btn_inventory_value_options = tk.Button(
    button_frame,
    text="Total Inventory Value",
    command=show_inventory_value_options,
    width=30
)
btn_inventory_value_options.pack(side=tk.LEFT, padx=5)

# Create a label for output display
output_label = tk.Label(
    window,
    text="Result:",
    fg="white",
    bg="black",
    font=("Arial", 18, "bold")
)
output_label.pack(pady=10)

# Create a scrollable output box with increased width and height
output_box = scrolledtext.ScrolledText(
    window,
    wrap=tk.WORD,
    width=100,
    height=35,
    font=("Arial", 12),
    bg="#cacaca",
    fg="black"
)
output_box.pack(pady=10)
output_box.config(state=tk.DISABLED)  # Make it read-only initially

# Start the Tkinter event loop
window.mainloop()