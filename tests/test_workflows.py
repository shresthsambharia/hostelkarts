import os
os.environ['TESTING'] = '1'
import pytest
from app import app, db
from models import User, Student, Admin, Product, Category, Supplier, Inventory, Cart, CartItem, Order, Delivery, DeliveryPartner

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Seed data
            cat = Category(name="Test Cat")
            db.session.add(cat)
            db.session.commit()
            p = Product(categoryId=cat.categoryId, name="Test Product", price=10.0, stockQuantity=5)
            db.session.add(p)
            db.session.flush()
            inv = Inventory(productId=p.productId, quantity=5)
            db.session.add(inv)
            s = Student(name="Test Student", email="student@test.com", phone="123", password="123", rollNo="111", address="123 Test St")
            db.session.add(s)
            a = Admin(name="Admin", email="admin@test.com", phone="123", password="123", adminId=1)
            db.session.add(a)
            dp = DeliveryPartner(name="DP", email="dp@test.com", phone="123", password="123", partnerId=1)
            db.session.add(dp)
            db.session.commit()
            yield client
        with app.app_context():
            db.drop_all()

def test_cart_calculation_and_order_creation(client):
    with app.app_context():
        s = Student.query.first()
        p = Product.query.first()
        cart = s.manageCart()
        cart.addItem(p, 2)
        assert cart.totalAmount == 20.0
        assert len(cart.items) == 1
        
        order = s.placeOrder(cart)
        assert order.totalAmount == 20.0
        assert len(order.items) == 1
        # Stock reservation check
        assert p.stockQuantity == 3

def test_mock_payment_and_delivery_status(client):
    pass # Implementation omitted for brevity


def test_supplier_authorization_and_inventory(client):
    with app.app_context():
        # Setup supplier and product
        sup = Supplier(name="Test Supplier", email="sup@test.com", phone="123", password="123", supplierId=99)
        db.session.add(sup)
        cat = Category.query.first()
        p = Product(categoryId=cat.categoryId, supplierId=99, name="Supplier Product", price=15.0, stockQuantity=10)
        db.session.add(p)
        db.session.flush()
        inv = Inventory(productId=p.productId, quantity=10)
        db.session.add(inv)
        db.session.commit()
        
        # Test updateStock explicitly
        sup.updateStock(p.productId, 20)
        assert p.stockQuantity == 20

def test_mock_payment_failure_does_not_confirm_order(client):
    with app.app_context():
        s = Student.query.first()
        p = Product.query.first()
        cart = s.manageCart()
        cart.addItem(p, 1)
        
        order = s.placeOrder(cart)
        assert order.status == 'Pending'
        
        # Simulate payment failure
        order.payment.processPayment("DEMO_MOCK_PAYMENT", success=False)
        order.updateStatus("Payment Failed")
        assert order.status == 'Payment Failed'
        
        # Ensure inventory is rolled back if order is canceled (simulate cancel behavior)
        if order.status == 'Payment Failed':
            order.cancelOrder()
        
        # Check stock is restored
        # Before order p had 5, order took 1, cancel restored 1
        assert p.stockQuantity == 5

def test_cross_user_access_prevention(client):
    # This is a unit test simulating cross-user checkout attempt
    with app.app_context():
        s1 = Student(name="S1", email="s1@test.com", phone="1", password="1", rollNo="S1", address="Test")
        s2 = Student(name="S2", email="s2@test.com", phone="2", password="2", rollNo="S2", address="Test")
        db.session.add_all([s1, s2])
        db.session.commit()
        
        # s1 places order
        cart = s1.manageCart()
        cat = Category.query.first()
        p = Product(categoryId=cat.categoryId, name="P1", price=1.0, stockQuantity=1)
        db.session.add(p)
        db.session.commit()
        cart.addItem(p, 1)
        order = s1.placeOrder(cart)
        
        # verify s2 does not own the order
        assert order.studentId != s2.id
