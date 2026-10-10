import os

base_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"

def write_file(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

write_file("README.md", """# HostelKart - Python OOP Mini Project

This is a fully functional web application developed with Python, Flask, and SQLite demonstrating Object-Oriented Programming principles and reproducing UML class and sequence diagrams.

## Features
- Complete UML class implementation with inheritance and associations.
- Role-based access for Students, Admins, and Delivery Partners.
- Shopping Cart and Checkout.
- Order management with price snapshots.
- Inventory tracking and validations.

## Setup Instructions
1. `python -m venv venv`
2. `venv\\Scripts\\activate` (Windows)
3. `pip install -r requirements.txt`
4. `python app.py`

## Demo Credentials
- Admin: admin@hostelkart.com / admin123
- Student: student@hostelkart.com / student123
- Delivery: partner@hostelkart.com / partner123

## Structure
- `models/`: Contains all UML mapped classes.
- `services/`: Contains business logic (e.g., placing orders, transaction handling).
- `templates/`: HTML views.
- `app.py`: Main Flask application.
""")

write_file("UML_CLASS_MAPPING.md", """# UML Class Mapping

| UML Class | Python File | Attributes Implemented | Methods Implemented |
|---|---|---|---|
| User | `models/user.py` | id, name, email, phone, password | register(), login(), updateProfile(), searchProducts() |
| Student | `models/student.py` | rollNo, hostel, address | placeOrder(), manageCart(), trackOrder(), rateDelivery() |
| Admin | `models/admin.py` | adminId, role | manageProducts(), manageInventory(), manageOrders(), manageUsers(), viewReports() |
| DeliveryPartner | `models/delivery_partner.py` | partnerId, vehicleNo, availability, location | receiveDeliveryRequest(), updateDeliveryStatus(), trackDelivery() |
| Category | `models/category.py` | categoryId, name, description | getProducts() |
| Product | `models/product.py` | productId, name, description, price, stockQuantity | getDetails(), getAvailability() |
| Supplier | `models/supplier.py` | supplierId, name, phone | supplyProducts(), updateStock() |
| Cart | `models/cart.py` | cartId, studentId, totalAmount | addItem(), removeItem(), updateQuantity(), calculateTotal() |
| CartItem | `models/cart.py` | cartItemId, productId, quantity, price | calculateSubtotal() |
| Order | `models/order.py` | orderId, studentId, orderDate, status, totalAmount | validateOrder(), generateOrder(), cancelOrder(), updateStatus() |
| OrderItem | `models/order.py` | orderItemId, productId, quantity, price | calculateSubtotal() |
| Payment | `models/payment.py` | paymentId, orderId, amount, method, status, transactionId | processPayment(), getPaymentStatus() |
| Inventory | `models/inventory.py` | inventoryId, productId, quantity, lastUpdated | checkAvailability(), updateStock() |
| Delivery | `models/delivery.py` | deliveryId, orderId, partnerId, status, deliveryAddress, assignedAt | assignPartner(), trackDelivery(), updateStatus() |
| Review | `models/review.py` | reviewId, studentId, productId, rating, comment | |
| Notification | `models/notification.py` | notificationId, userId, type, message, sentAt | sendNotification() |

## Text-Based Class Hierarchy
User (Base)
├── Student
├── Admin
└── DeliveryPartner

## Sequence-Workflow Explanation
1. **Search & Cart**: Student accesses `/product/<id>`, adds to cart via `add_to_cart()`. Product availability is checked. `CartItem` created.
2. **Order**: Cart checkout calls `OrderService.create_order_from_cart`. Validates stock, locks prices, deducts inventory.
3. **Delivery**: Order creates a `Delivery`. Delivery partner updates status in `/delivery`.
""")

write_file("demo_oop.py", """from app import app, db
from models import *

def run_demo():
    with app.app_context():
        print("=== OOP DEMONSTRATION ===")
        
        student = Student.query.filter_by(email='student@hostelkart.com').first()
        print(f"1. Is student an instance of Student? {isinstance(student, Student)}")
        print(f"2. Is student an instance of User (Inheritance)? {isinstance(student, User)}")
        
        product = Product.query.first()
        print(f"3. Product retrieved: {product.name} (Stock: {product.stockQuantity})")
        
        cart = student.manageCart()
        cart.addItem(product, 2)
        print(f"4. Added 2 items to cart. Cart Total: {cart.calculateTotal()}")
        
        try:
            order = student.placeOrder(cart)
            print(f"5. Order Placed Successfully! Order ID: {order.orderId}, Total: {order.totalAmount}")
            print(f"6. Stock after order: {Product.query.get(product.productId).stockQuantity}")
        except Exception as e:
            print(f"Error placing order: {e}")
            
        print("=== DEMO COMPLETE ===")

if __name__ == '__main__':
    run_demo()
""")

write_file("tests/__init__.py", "")

write_file("tests/test_models.py", """import pytest
from app import app, db
from models import User, Student, Product, Category

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        with app.app_context():
            db.drop_all()

def test_inheritance(client):
    s = Student(name="Test", email="test@test.com", phone="123", password="123", rollNo="111")
    assert isinstance(s, User)
    assert isinstance(s, Student)
""")

print("Docs and tests generated.")
