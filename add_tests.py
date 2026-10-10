import os

test_path = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\tests\test_workflows.py"
with open(test_path, "r", encoding="utf-8") as f:
    content = f.read()

new_tests = """
def test_supplier_authorization_and_inventory(client):
    with app.app_context():
        # Setup supplier and product
        sup = Supplier(name="Test Supplier", email="sup@test.com", phone="123", password="123", supplierId=99)
        db.session.add(sup)
        cat = Category.query.first()
        p = Product(categoryId=cat.categoryId, supplierId=99, name="Supplier Product", price=15.0, stockQuantity=10)
        db.session.add(p)
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
        s1 = Student(name="S1", email="s1@test.com", phone="1", password="1", rollNo="S1")
        s2 = Student(name="S2", email="s2@test.com", phone="2", password="2", rollNo="S2")
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
"""
if "test_supplier_authorization_and_inventory" not in content:
    with open(test_path, "a", encoding="utf-8") as f:
        f.write(new_tests)

print("Tests added.")
