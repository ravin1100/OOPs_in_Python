from collections import defaultdict

class Product:
    totol_products = 0
    category_counter = defaultdict(int)

    def __init__(self, id, name, price, category, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.quantity = quantity

        Product.totol_products += 1
        Product.category_counter[category] += 1

    def get_product_info(self):
        return f"{self.name} (${self.price}) - Category: {self.category}, Stock: {self.stock_quantity}"

    def stock_quantity(self):
        return self.quantity 
    
    @classmethod
    def get_total_products(cls):
        return cls.totol_products
    
    @classmethod
    def get_most_popular_category(cls):
        if not cls.category_counter:
            return None
        return max(cls.category_counter, key = cls.category_counter.get)
    
    def reduce_stock(self, quantity):
        if self.quantity >= quantity:
            self.quantity -= quantity
            return True
        return False
    
    def __str__(self):
        return self.get_product_info()
    

class Customer:
    total_revenue = 0

    def __init__(self, id, name, email, customer_type = "regular"):
        self.id = id
        self.name = name
        self.email = email
        self.customer_type = customer_type

    def get_discount_rate(self):
        discount_rate = {
            'regular':0,
            'premium':10,
            'vip':20
        } 
        return discount_rate.get(self.customer_type, 0)
    
    def add_revenue(self, amount):
        Customer.total_revenue += amount

    @classmethod
    def get_total_revenue(cls):
        return round(cls.total_revenue, 2)
    
    def __str__(self):
        return f"{self.name} ({self.customer_type.title()})"




class ShoppingCart:
    
    def __init__(self, customer):
        self.customer = customer
        self.items = {}

    def add_item(self, product, quantity):
        if product.id in self.items:
            self.items[product.id] = (product, self.items[product.id][1] + quantity)
        else:
            self.items[product.id] = (product, quantity)

    def remove_item(self, id):
        if id in self.items:
            del self.items[id]

    def clear_cart(self):
        self.items.clear()

    def get_total_items(self):
        return sum(quantity for _, quantity in self.items.values())
    
    def get_subtotal(self):
        return round(sum(product.price*quantity for product, quantity in self.items.values()), 2)
    
    def calculate_total(self):
        sub_total = self.get_subtotal()
        discount = (self.customer.get_discount_rate()/100) * sub_total
        return round(sub_total-discount, 2)
    
    def get_cart_items(self):
        return [(product.name, quantity) for product, quantity in self.items.values()]
    
    def place_order(self):
        for product, quantity in self.items.values():
            if product.quantity < quantity:
                return f"Order failed, Insufficient stock"
        
        total = self.calculate_total()

        for product, quantity in self.items.values():
            product.reduce_stock(quantity)

        self.customer.add_revenue(total)
        self.clear_cart()
        return f"Order placed successfully! Total: ${total}"
        

    



# Test Case 1: Creating products with different categories
laptop = Product("P001", "Gaming Laptop", 1299.99, "Electronics", 10)
book = Product("P002", "Python Programming", 49.99, "Books", 25)
shirt = Product("P003", "Cotton T-Shirt", 19.99, "Clothing", 50)

print(f"Product info: {laptop.get_product_info()}")
print(f"Total products in system: {Product.get_total_products()}")

# Test Case 2: Creating customer and shopping cart
customer = Customer("C001", "John Doe", "john@email.com", "premium")
cart = ShoppingCart(customer)

print(f"Customer: {customer}")
print(f"Customer discount: {customer.get_discount_rate()}%")

# Test Case 3: Adding items to cart
cart.add_item(laptop, 1)
cart.add_item(book, 2)
cart.add_item(shirt, 3)

print(f"Cart total items: {cart.get_total_items()}")
print(f"Cart subtotal: ${cart.get_subtotal()}")

# Test Case 4: Applying discounts and calculating final price
final_total = cart.calculate_total()
print(f"Final total (with {customer.get_discount_rate()}% discount): ${final_total}")

# Test Case 5: Inventory management
print(f"Laptop stock before order: {laptop.quantity}")
order_result = cart.place_order()
print(f"Order result: {order_result}")
print(f"Laptop stock after order: {laptop.quantity}")

# Test Case 6: Class methods for business analytics
popular_category = Product.get_most_popular_category()
print(f"Most popular category: {popular_category}")

total_revenue = Customer.get_total_revenue()
print(f"Total revenue: ${total_revenue}")

# Test Case 7: Cart operations
cart.remove_item("P002")  # Remove book
print(f"Items after removal: {cart.get_cart_items()}")

cart.clear_cart()
print(f"Items after clearing: {cart.get_total_items()}")

# Expected outputs should show proper product management, cart operations,
# discount calculations, inventory updates, and business analytics