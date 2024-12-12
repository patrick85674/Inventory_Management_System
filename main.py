#test test test :)

# from inventory.product import Product
from inventory.inventory_manager import InventoryManager
from inventory.product_data import products

# Initialize inventory manager
inventory = InventoryManager()

# Add products from the imported data
for prod in products:
    product = Product(prod["id"], prod["name"], prod["price"], prod["quantity"], prod["category"])
    inventory.add_product(product)

# Example operations:

# Print all products
print("All products in inventory:")
for product_name in inventory._products:
    print(inventory.get_product_info(product_name))

# Update quantity of a product
inventory.update_product_quantity("Laptop", 15)
print("\nUpdated Laptop quantity:")
print(inventory.get_product_info("Laptop"))

# Get total inventory value
print(f"\nTotal Inventory Value: {inventory.get_total_inventory_value()}")

# Search for products
print("\nSearch results for 'phone':")
search_results = inventory.search_product("phone")
if isinstance(search_results, list):
    for result in search_results:
        print(result)
else:
    print(search_results)
