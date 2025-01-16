from django.core.management.base import BaseCommand
from threading import Thread, Lock
from users.models import User
from products.models import Product
from orders.models import Order

class Command(BaseCommand):
    help = 'Insert data into users, products, and orders databases with threading'

    def handle(self, *args, **kwargs):
        self.emails_set = set()
        self.product_names_set = set()
        self.users = []
        self.products = []
        self.lock = Lock() 

        users_data = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
            {"id": 4, "name": "David", "email": "david@example.com"},
            {"id": 5, "name": "Eve", "email": "eve@example.com"},
            {"id": 6, "name": "Frank", "email": "frank@example.com"},
            {"id": 7, "name": "Grace", "email": "grace@example.com"},
            {"id": 8, "name": "Alice", "email": "alice@example.com"},
            {"id": 9, "name": "Henry", "email": "henry@example.com"},
            {"id": 10, "name": "", "email": "jane@example.com"},
        ]

        products_data = [
            {"id": 1, "name": "Laptop", "price": 1000.00},
            {"id": 2, "name": "Smartphone", "price": 700.00},
            {"id": 3, "name": "Headphones", "price": 150.00},
            {"id": 4, "name": "Monitor", "price": 300.00},
            {"id": 5, "name": "Keyboard", "price": 50.00},
            {"id": 6, "name": "Mouse", "price": 30.00},
            {"id": 7, "name": "Laptop", "price": 1000.00},
            {"id": 8, "name": "Smartwatch", "price": 250.00},
            {"id": 9, "name": "Gaming Chair", "price": 500.00},
            {"id": 10, "name": "Earbuds", "price": -50.00},
        ]

        orders_data = [
            {"id": 1, "user_id": 1, "product_id": 1, "quantity": 2},
            {"id": 2, "user_id": 2, "product_id": 2, "quantity": 1},
            {"id": 3, "user_id": 3, "product_id": 3, "quantity": 5},
            {"id": 4, "user_id": 4, "product_id": 4, "quantity": 1},
            {"id": 5, "user_id": 5, "product_id": 5, "quantity": 3},
            {"id": 6, "user_id": 6, "product_id": 6, "quantity": 4},
            {"id": 7, "user_id": 7, "product_id": 7, "quantity": 2},
            {"id": 8, "user_id": 8, "product_id": 8, "quantity": 0},
            {"id": 9, "user_id": 9, "product_id": 1, "quantity": -1},
            {"id": 10, "user_id": 10, "product_id": 11, "quantity": 2},
        ]

        threads = [
            Thread(target=self.insert_users, args=(users_data,)),
            Thread(target=self.insert_products, args=(products_data,)),
            Thread(target=self.insert_orders, args=(orders_data,)),
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def insert_users(self, users_data):
        for user in users_data:
            try:
                if user["name"] and user["email"]:
                    with self.lock:
                        if user["email"] not in self.emails_set:
                            User.objects.create(**user)
                            self.emails_set.add(user["email"])
                            self.users.append(user)
                            print(f"Inserted User: {user['name']}")
                        else:
                            print(f"Email Already Exists: {user['email']}")
                else:
                    print(f"Invalid User Data: {user}")
            except Exception as e:
                print(f"Error inserting user: {e}")

    def insert_products(self, products_data):
        for product in products_data:
            try:
                if product["price"] > 0:
                    with self.lock:
                        if product["name"].lower() not in self.product_names_set:
                            Product.objects.create(**product)
                            self.product_names_set.add(product["name"].lower())
                            self.products.append(product)
                            print(f"Inserted Product: {product['name']}")
                        else:
                            print(f"Product Already Exists: {product['name']}")
                else:
                    print(f"Invalid Product Price: {product['name']}")
            except Exception as e:
                print(f"Error inserting product: {e}")

    def insert_orders(self, orders_data):
        for order in orders_data:
            try:
                with self.lock:
                    if any(user["id"] == order["user_id"] for user in self.users):
                        if any(product["id"] == order["product_id"] for product in self.products):
                            if order["quantity"] > 0:
                                Order.objects.create(**order)
                                print(f"Inserted Order: {order}")
                            else:
                                print(f"Invalid Order Quantity: {order}")
                        else:
                            print(f"Invalid Product ID in Order: {order}")
                    else:
                        print(f"Invalid User ID in Order: {order}")
            except Exception as e:
                print(f"Error inserting order: {e}")
