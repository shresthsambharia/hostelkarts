from app import app, db
from models import *

def run_demo():
    with app.app_context():
        from app import setup_database
        setup_database()
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
            print(f"6. Stock after order: {db.session.get(Product, product.productId).stockQuantity}")
        except Exception as e:
            print(f"Error placing order: {e}")
            
        print("=== DEMO COMPLETE ===")

if __name__ == '__main__':
    run_demo()
