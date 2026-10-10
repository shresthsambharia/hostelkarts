from app import app
from database import db
from models.category import Category
from models.supplier import Supplier
from models.product import Product
from models.inventory import Inventory

categories_data = [
    {"name": "Instant Food & Snacks", "description": "Quick meals and late night bites"},
    {"name": "Biscuits & Packaged Snacks", "description": "Cookies, chips, and munchies"},
    {"name": "Beverages", "description": "Juices, tea, coffee, and water"},
    {"name": "Personal Care", "description": "Soap, shampoo, toothpaste, etc."},
    {"name": "Hygiene & Laundry", "description": "Detergent, tissues, cleaning"},
    {"name": "Stationery", "description": "Notebooks, pens, study materials"},
    {"name": "Daily Essentials", "description": "Storage, locks, umbrellas"},
    {"name": "Electrical Accessories", "description": "Extensions, chargers, earphones"}
]

products_data = [
    # Instant Food
    ("Pasta Packet", "Instant Food & Snacks", 25.0, 40),
    ("Cup Noodles (Spicy)", "Instant Food & Snacks", 40.0, 50),
    ("Cup Noodles (Veg)", "Instant Food & Snacks", 40.0, 50),
    ("Oats Pack", "Instant Food & Snacks", 60.0, 30),
    ("Tomato Ketchup Sachet", "Instant Food & Snacks", 2.0, 200),
    ("Peanut Butter (Small)", "Instant Food & Snacks", 120.0, 15),
    ("Mixed Fruit Jam", "Instant Food & Snacks", 85.0, 20),
    
    # Biscuits & Packaged Snacks
    ("Potato Chips (Salted)", "Biscuits & Packaged Snacks", 20.0, 100),
    ("Potato Chips (Masala)", "Biscuits & Packaged Snacks", 20.0, 100),
    ("Chocolate Cookies", "Biscuits & Packaged Snacks", 30.0, 60),
    ("Digestive Biscuits", "Biscuits & Packaged Snacks", 40.0, 45),
    ("Roasted Peanuts", "Biscuits & Packaged Snacks", 15.0, 80),
    ("Nachos Cheese", "Biscuits & Packaged Snacks", 35.0, 40),
    ("Energy Bar", "Biscuits & Packaged Snacks", 40.0, 50),
    ("Cream Biscuits", "Biscuits & Packaged Snacks", 25.0, 70),
    
    # Beverages
    ("Apple Juice Box", "Beverages", 20.0, 120),
    ("Mango Drink", "Beverages", 20.0, 100),
    ("Cold Coffee Can", "Beverages", 50.0, 40),
    ("Tea Bags (25 pcs)", "Beverages", 60.0, 30),
    ("Instant Coffee Powder", "Beverages", 90.0, 25),
    ("Mineral Water (1L)", "Beverages", 20.0, 150),
    ("Energy Drink Can", "Beverages", 110.0, 20),
    
    # Personal Care
    ("Bathing Soap", "Personal Care", 35.0, 100),
    ("Anti-Dandruff Shampoo", "Personal Care", 150.0, 30),
    ("Toothpaste (100g)", "Personal Care", 55.0, 80),
    ("Toothbrush (Soft)", "Personal Care", 30.0, 100),
    ("Deodorant Spray", "Personal Care", 199.0, 25),
    ("Face Wash", "Personal Care", 120.0, 40),
    ("Hair Oil", "Personal Care", 75.0, 45),
    ("Moisturizing Lotion", "Personal Care", 140.0, 20),
    
    # Hygiene & Laundry
    ("Washing Powder (500g)", "Hygiene & Laundry", 65.0, 60),
    ("Liquid Detergent", "Hygiene & Laundry", 150.0, 30),
    ("Dishwash Bar", "Hygiene & Laundry", 15.0, 100),
    ("Tissue Paper Box", "Hygiene & Laundry", 50.0, 70),
    ("Garbage Bags (30 pcs)", "Hygiene & Laundry", 60.0, 50),
    ("Room Freshener", "Hygiene & Laundry", 110.0, 20),
    ("Hand Sanitizer", "Hygiene & Laundry", 50.0, 80),
    
    # Stationery
    ("A4 Notebook (Ruled)", "Stationery", 45.0, 150),
    ("A4 Notebook (Unruled)", "Stationery", 45.0, 100),
    ("Blue Ballpoint Pen", "Stationery", 10.0, 300),
    ("Black Ballpoint Pen", "Stationery", 10.0, 200),
    ("Highlighter Set (3 colors)", "Stationery", 60.0, 40),
    ("Sticky Notes", "Stationery", 40.0, 60),
    ("Geometry Box", "Stationery", 90.0, 15),
    ("Stapler & Pins", "Stationery", 75.0, 25),
    
    # Daily Essentials
    ("Padlock with Keys", "Daily Essentials", 150.0, 20),
    ("Umbrella", "Daily Essentials", 350.0, 15),
    ("Plastic Storage Box", "Daily Essentials", 200.0, 10),
    ("Nail Clipper", "Daily Essentials", 40.0, 50),
    
    # Electrical Accessories
    ("3-Pin Extension Board", "Electrical Accessories", 250.0, 15),
    ("USB-C Charging Cable", "Electrical Accessories", 150.0, 30),
    ("Micro-USB Cable", "Electrical Accessories", 100.0, 25),
    ("Earphones (Wired)", "Electrical Accessories", 299.0, 20),
    ("Table Lamp", "Electrical Accessories", 450.0, 10)
]

def seed_products():
    with app.app_context():
        print(f"Products before seeding: {Product.query.count()}")
        
        # Ensure supplier exists
        supplier = Supplier.query.first()
        if not supplier:
            supplier = Supplier(name="Campus Store", email="supplier@hostelkart.com", phone="9988776655", supplierId=1)
            supplier.register("supplier123")
            db.session.add(supplier)
            db.session.commit()
            
        # Add categories
        cat_map = {}
        for c in categories_data:
            cat = Category.query.filter_by(name=c["name"]).first()
            if not cat:
                cat = Category(name=c["name"], description=c["description"])
                db.session.add(cat)
                db.session.commit()
            cat_map[c["name"]] = cat.categoryId
            
        # Add products
        added_count = 0
        for name, cat_name, price, stock in products_data:
            cat_id = cat_map[cat_name]
            prod = Product.query.filter_by(name=name).first()
            if not prod:
                prod = Product(categoryId=cat_id, supplierId=supplier.supplierId, name=name, description=f"{name} - {cat_name}", price=price, stockQuantity=stock)
                db.session.add(prod)
                db.session.commit()
                
                inv = Inventory(productId=prod.productId, quantity=stock)
                db.session.add(inv)
                db.session.commit()
                added_count += 1
                
        print(f"Products added: {added_count}")
        print(f"Products after seeding: {Product.query.count()}")

if __name__ == '__main__':
    seed_products()
