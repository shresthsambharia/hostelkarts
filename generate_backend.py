import os
import sys

base_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"

def write_file(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

# ----------------- APP AND CONFIG -----------------
write_file("requirements.txt", """Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.0
pytest==7.4.2
""")

write_file("config.py", """import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-for-demo'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hostelkart.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
""")

write_file("database.py", """from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
""")

# ----------------- MODELS -----------------
write_file("models/__init__.py", """from database import db
from .user import User
from .student import Student
from .admin import Admin
from .delivery_partner import DeliveryPartner
from .category import Category
from .product import Product
from .supplier import Supplier
from .cart import Cart, CartItem
from .order import Order, OrderItem
from .payment import Payment
from .inventory import Inventory
from .delivery import Delivery
from .review import Review
from .notification import Notification
""")

write_file("models/user.py", """from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def register(self, raw_password):
        self.password = generate_password_hash(raw_password)
        db.session.add(self)
        db.session.commit()

    def login(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def updateProfile(self, name, phone):
        self.name = name
        self.phone = phone
        db.session.commit()

    def searchProducts(self, query):
        from models.product import Product
        return Product.query.filter(Product.name.ilike(f'%{query}%')).all()
""")

write_file("models/student.py", """from database import db
from .user import User

class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    rollNo = db.Column(db.String(20), unique=True)
    hostel = db.Column(db.String(50))
    address = db.Column(db.String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def placeOrder(self, cart):
        from services.order_service import OrderService
        return OrderService.create_order_from_cart(self, cart)

    def manageCart(self):
        from models.cart import Cart
        cart = Cart.query.filter_by(studentId=self.id).first()
        if not cart:
            cart = Cart(studentId=self.id)
            db.session.add(cart)
            db.session.commit()
        return cart

    def trackOrder(self, orderId):
        from models.order import Order
        return Order.query.filter_by(orderId=orderId, studentId=self.id).first()

    def rateDelivery(self, deliveryId, rating, comment):
        from models.review import Review
        review = Review(studentId=self.id, deliveryId=deliveryId, rating=rating, comment=comment)
        db.session.add(review)
        db.session.commit()
        return review
""")

write_file("models/admin.py", """from database import db
from .user import User

class Admin(User):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    adminId = db.Column(db.Integer, unique=True)
    role = db.Column(db.String(50), default="SuperAdmin")

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def manageProducts(self):
        from models.product import Product
        return Product.query.all()

    def manageInventory(self):
        from models.inventory import Inventory
        return Inventory.query.all()

    def manageOrders(self):
        from models.order import Order
        return Order.query.all()

    def manageUsers(self):
        return User.query.all()

    def viewReports(self):
        pass
""")

write_file("models/delivery_partner.py", """from database import db
from .user import User

class DeliveryPartner(User):
    __tablename__ = 'delivery_partners'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    partnerId = db.Column(db.Integer, unique=True)
    vehicleNo = db.Column(db.String(20))
    availability = db.Column(db.Boolean, default=True)
    location = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'delivery_partner',
    }

    def receiveDeliveryRequest(self):
        from models.delivery import Delivery
        return Delivery.query.filter_by(partnerId=self.id, status='Assigned').all()

    def updateDeliveryStatus(self, deliveryId, status):
        from models.delivery import Delivery
        delivery = Delivery.query.get(deliveryId)
        if delivery and delivery.partnerId == self.id:
            delivery.updateStatus(status)
            return True
        return False

    def trackDelivery(self, deliveryId):
        from models.delivery import Delivery
        return Delivery.query.get(deliveryId)
""")

write_file("models/category.py", """from database import db

class Category(db.Model):
    __tablename__ = 'categories'
    categoryId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    products = db.relationship('Product', backref='category', lazy=True)

    def getProducts(self):
        return self.products
""")

write_file("models/product.py", """from database import db

class Product(db.Model):
    __tablename__ = 'products'
    productId = db.Column(db.Integer, primary_key=True)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.categoryId'), nullable=False)
    supplierId = db.Column(db.Integer, db.ForeignKey('suppliers.supplierId'), nullable=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stockQuantity = db.Column(db.Integer, default=0)

    inventory = db.relationship('Inventory', backref='product', uselist=False)

    def getDetails(self):
        return {
            'productId': self.productId,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stockQuantity': self.stockQuantity
        }

    def getAvailability(self):
        return self.stockQuantity > 0
""")

write_file("models/supplier.py", """from database import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    supplierId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))

    products = db.relationship('Product', backref='supplier', lazy=True)

    def supplyProducts(self, product, quantity):
        product.stockQuantity += quantity
        if product.inventory:
            product.inventory.quantity += quantity
        db.session.commit()

    def updateStock(self, productId, quantity):
        from models.inventory import Inventory
        inv = Inventory.query.filter_by(productId=productId).first()
        if inv:
            inv.updateStock(quantity)
""")

write_file("models/cart.py", """from database import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    cartItemId = db.Column(db.Integer, primary_key=True)
    cartId = db.Column(db.Integer, db.ForeignKey('carts.cartId'), nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('products.productId'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)

    product = db.relationship('Product')

    def calculateSubtotal(self):
        return self.quantity * self.price

class Cart(db.Model):
    __tablename__ = 'carts'
    cartId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    totalAmount = db.Column(db.Float, default=0.0)

    items = db.relationship('CartItem', backref='cart', lazy=True, cascade="all, delete-orphan")

    def addItem(self, product, quantity=1):
        item = CartItem.query.filter_by(cartId=self.cartId, productId=product.productId).first()
        if item:
            item.quantity += quantity
        else:
            item = CartItem(cartId=self.cartId, productId=product.productId, quantity=quantity, price=product.price)
            db.session.add(item)
        self.calculateTotal()
        db.session.commit()

    def removeItem(self, productId):
        item = CartItem.query.filter_by(cartId=self.cartId, productId=productId).first()
        if item:
            db.session.delete(item)
            self.calculateTotal()
            db.session.commit()

    def updateQuantity(self, productId, quantity):
        item = CartItem.query.filter_by(cartId=self.cartId, productId=productId).first()
        if item:
            item.quantity = quantity
            self.calculateTotal()
            db.session.commit()

    def calculateTotal(self):
        total = sum(item.calculateSubtotal() for item in self.items)
        self.totalAmount = total
        return total
""")

write_file("models/order.py", """from database import db
from datetime import datetime

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    orderItemId = db.Column(db.Integer, primary_key=True)
    orderId = db.Column(db.Integer, db.ForeignKey('orders.orderId'), nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('products.productId'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Immutable snapshot of price at order time

    product = db.relationship('Product')

    def calculateSubtotal(self):
        return self.quantity * self.price

class Order(db.Model):
    __tablename__ = 'orders'
    orderId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    orderDate = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Pending")
    totalAmount = db.Column(db.Float, nullable=False)

    items = db.relationship('OrderItem', backref='order', lazy=True)
    payment = db.relationship('Payment', backref='order', uselist=False)
    delivery = db.relationship('Delivery', backref='order', uselist=False)

    def validateOrder(self):
        # Validation is usually done before creation, ensuring stock etc.
        return len(self.items) > 0

    def generateOrder(self):
        # Implementation of generating invoice/details
        pass

    def cancelOrder(self):
        if self.status in ['Pending', 'Confirmed']:
            self.status = 'Cancelled'
            # Restore inventory
            for item in self.items:
                if item.product.inventory:
                    item.product.inventory.quantity += item.quantity
                item.product.stockQuantity += item.quantity
            db.session.commit()
            return True
        return False

    def updateStatus(self, new_status):
        self.status = new_status
        db.session.commit()
""")

write_file("models/payment.py", """from database import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'
    paymentId = db.Column(db.Integer, primary_key=True)
    orderId = db.Column(db.Integer, db.ForeignKey('orders.orderId'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Pending')
    transactionId = db.Column(db.String(100), unique=True, nullable=True)

    def processPayment(self, method_name, success=True):
        import uuid
        self.method = method_name
        if success:
            self.status = 'Success'
            self.transactionId = "TXN" + str(uuid.uuid4()).replace("-", "")[:10].upper()
        else:
            self.status = 'Failed'
        db.session.commit()
        return self.status == 'Success'

    def getPaymentStatus(self):
        return self.status
""")

write_file("models/inventory.py", """from database import db
from datetime import datetime

class Inventory(db.Model):
    __tablename__ = 'inventory'
    inventoryId = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, db.ForeignKey('products.productId'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def checkAvailability(self, req_qty):
        return self.quantity >= req_qty

    def updateStock(self, new_qty):
        if new_qty < 0:
            raise ValueError("Inventory cannot be negative")
        self.quantity = new_qty
        self.product.stockQuantity = new_qty
        db.session.commit()
""")

write_file("models/delivery.py", """from database import db
from datetime import datetime

class Delivery(db.Model):
    __tablename__ = 'deliveries'
    deliveryId = db.Column(db.Integer, primary_key=True)
    orderId = db.Column(db.Integer, db.ForeignKey('orders.orderId'), nullable=False)
    partnerId = db.Column(db.Integer, db.ForeignKey('delivery_partners.id'), nullable=True)
    status = db.Column(db.String(50), default='Pending')
    deliveryAddress = db.Column(db.String(255), nullable=False)
    assignedAt = db.Column(db.DateTime, nullable=True)

    def assignPartner(self, partnerId):
        self.partnerId = partnerId
        self.status = 'Assigned'
        self.assignedAt = datetime.utcnow()
        db.session.commit()

    def trackDelivery(self):
        return self.status

    def updateStatus(self, new_status):
        self.status = new_status
        db.session.commit()
        
        # Consistent order update
        if self.order:
            if new_status == 'Delivered':
                self.order.updateStatus('Completed')
            else:
                self.order.updateStatus(new_status)
""")

write_file("models/review.py", """from database import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'
    reviewId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('products.productId'), nullable=True)
    deliveryId = db.Column(db.Integer, db.ForeignKey('deliveries.deliveryId'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
""")

write_file("models/notification.py", """from database import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'
    notificationId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50))
    message = db.Column(db.Text, nullable=False)
    sentAt = db.Column(db.DateTime, default=datetime.utcnow)

    def sendNotification(self):
        # Implementation of push/email notification
        pass
""")

# ----------------- SERVICES -----------------
write_file("services/__init__.py", "")

write_file("services/order_service.py", """from database import db
from models.order import Order, OrderItem
from models.payment import Payment
from models.inventory import Inventory
from models.product import Product
from models.delivery import Delivery

class OrderService:
    @staticmethod
    def create_order_from_cart(student, cart):
        if not cart.items:
            raise ValueError("Cart is empty")

        # Start transaction logically
        try:
            total = 0
            order = Order(studentId=student.id, totalAmount=0, status='Pending')
            db.session.add(order)
            db.session.flush() # Get orderId

            for c_item in cart.items:
                product = Product.query.with_for_update().get(c_item.productId)
                if not product or product.stockQuantity < c_item.quantity:
                    db.session.rollback()
                    raise ValueError(f"Not enough stock for {product.name if product else 'unknown product'}")
                
                # Update inventory
                product.stockQuantity -= c_item.quantity
                if product.inventory:
                    product.inventory.quantity -= c_item.quantity
                
                o_item = OrderItem(
                    orderId=order.orderId,
                    productId=product.productId,
                    quantity=c_item.quantity,
                    price=product.price # Price at order time snapshot
                )
                db.session.add(o_item)
                total += o_item.calculateSubtotal()
            
            order.totalAmount = total
            
            # Empty cart
            for c_item in cart.items:
                db.session.delete(c_item)
            cart.totalAmount = 0
            
            # Setup payment and delivery
            payment = Payment(orderId=order.orderId, amount=total)
            db.session.add(payment)
            
            delivery = Delivery(orderId=order.orderId, deliveryAddress=student.address)
            db.session.add(delivery)
            
            db.session.commit()
            return order
        except Exception as e:
            db.session.rollback()
            raise e
""")

# ----------------- MAIN APP -----------------
write_file("app.py", """from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db
from config import Config
from models import *
from services.order_service import OrderService

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def setup_database():
    with app.app_context():
        db.create_all()
        # Seed basic data
        if not Admin.query.filter_by(email='admin@hostelkart.com').first():
            admin = Admin(name="Super Admin", email="admin@hostelkart.com", phone="1234567890", adminId=1, role="SuperAdmin")
            admin.register("admin123")
            
            student = Student(name="John Doe", email="student@hostelkart.com", phone="0987654321", rollNo="S001", hostel="Boys Hostel A", address="Room 101, Hostel A")
            student.register("student123")
            
            partner = DeliveryPartner(name="Speedy Deliveries", email="partner@hostelkart.com", phone="1122334455", partnerId=1, vehicleNo="AB12CD3456", location="Campus Gate")
            partner.register("partner123")
            
            cat = Category(name="Snacks", description="Late night cravings")
            db.session.add(cat)
            db.session.commit()
            
            sup = Supplier(name="Campus Store", phone="9988776655")
            db.session.add(sup)
            db.session.commit()
            
            prod = Product(categoryId=cat.categoryId, supplierId=sup.supplierId, name="Maggi Noodles", description="Instant Noodles", price=20.0, stockQuantity=50)
            db.session.add(prod)
            db.session.commit()
            
            inv = Inventory(productId=prod.productId, quantity=50)
            db.session.add(inv)
            db.session.commit()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.login(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            if isinstance(user, Admin):
                return redirect(url_for('admin_dashboard'))
            elif isinstance(user, DeliveryPartner):
                return redirect(url_for('delivery_dashboard'))
            else:
                return redirect(url_for('index'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    if not isinstance(current_user, Student):
        flash('Only students can add items to cart.', 'danger')
        return redirect(url_for('index'))
    
    qty = int(request.form.get('quantity', 1))
    product = Product.query.get_or_404(product_id)
    
    if product.stockQuantity < qty:
        flash('Not enough stock available.', 'danger')
        return redirect(url_for('product_detail', product_id=product_id))
    
    cart = current_user.manageCart()
    cart.addItem(product, qty)
    flash('Item added to cart.', 'success')
    return redirect(url_for('cart'))

@app.route('/cart')
@login_required
def cart():
    if not isinstance(current_user, Student):
        return redirect(url_for('index'))
    cart = current_user.manageCart()
    return render_template('cart.html', cart=cart)

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    if not isinstance(current_user, Student):
        return redirect(url_for('index'))
    cart = current_user.manageCart()
    try:
        order = current_user.placeOrder(cart)
        return redirect(url_for('payment', order_id=order.orderId))
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('cart'))

@app.route('/payment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def payment(order_id):
    order = Order.query.get_or_404(order_id)
    if request.method == 'POST':
        action = request.form.get('action')
        success = (action == 'success')
        order.payment.processPayment("Credit Card Mock", success=success)
        if success:
            order.updateStatus("Confirmed")
            flash("Payment successful. Order placed!", "success")
        else:
            flash("Payment failed.", "danger")
        return redirect(url_for('orders'))
    return render_template('checkout.html', order=order)

@app.route('/orders')
@login_required
def orders():
    if isinstance(current_user, Student):
        orders = Order.query.filter_by(studentId=current_user.id).all()
        return render_template('orders.html', orders=orders)
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        return "Unauthorized", 403
    return render_template('admin_dashboard.html')

@app.route('/delivery')
@login_required
def delivery_dashboard():
    if not isinstance(current_user, DeliveryPartner):
        return "Unauthorized", 403
    deliveries = current_user.receiveDeliveryRequest()
    return render_template('delivery_dashboard.html', deliveries=deliveries)

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
""")

print("Done writing backend files.")
