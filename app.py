from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db
from config import Config
from models import *
from services.order_service import OrderService

app = Flask(__name__)
app.config.from_object(Config)
import os
if os.environ.get('TESTING'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def setup_database():
    with app.app_context():
        db.create_all()
        if not HostelGroup.query.first():
            db.session.add(HostelGroup(name='Block A Freshers', description='Discussions for Block A'))
            db.session.add(HostelGroup(name='Late Night Snacking', description='Order together to save delivery fee'))
            db.session.commit()

        # Seed basic data
        if not Admin.query.filter_by(email='admin@hostelkart.com').first():
            admin = Admin(name="Super Admin", email="admin@hostelkart.com", phone="1234567890", adminId=1, role="SuperAdmin")
            admin.register("admin123")
            
        if not Student.query.filter_by(email='student@hostelkart.com').first():
            student = Student(name="John Doe", email="student@hostelkart.com", phone="0987654321", rollNo="S001", hostel="Boys Hostel A", address="Room 101, Hostel A")
            student.register("student123")
            
        if not DeliveryPartner.query.filter_by(email='partner@hostelkart.com').first():
            partner = DeliveryPartner(name="Speedy Deliveries", email="partner@hostelkart.com", phone="1122334455", partnerId=1, vehicleNo="AB12CD3456", location="Campus Gate")
            partner.register("partner123")
            
        if not DeliveryPartner.query.filter_by(email='delivery@hostelkart.com').first():
            dp = DeliveryPartner(name='Delivery Boy', email='delivery@hostelkart.com', phone='555666777', password='tmp', partnerId='DP001', vehicleNo='XYZ-123')
            dp.register('delivery123')

        if not Supplier.query.filter_by(email='supplier@hostelkart.com').first():
            sup = Supplier(name="Campus Store", email="supplier@hostelkart.com", phone="9988776655", supplierId=1)
            sup.register("supplier123")
            
        cat = Category.query.filter_by(name="Snacks").first()
        if not cat:
            cat = Category(name="Snacks", description="Late night cravings")
            db.session.add(cat)
            db.session.commit()
            
        prod = Product.query.filter_by(name="Maggi Noodles").first()
        if not prod:
            sup = Supplier.query.filter_by(email='supplier@hostelkart.com').first()
            prod = Product(categoryId=cat.categoryId, supplierId=sup.supplierId, name="Maggi Noodles", description="Instant Noodles", price=20.0, stockQuantity=50)
            db.session.add(prod)
            db.session.commit()
            
            inv = Inventory(productId=prod.productId, quantity=50)
            db.session.add(inv)
            db.session.commit()

@app.route('/')
def index():
    category_id = request.args.get('category_id')
    if category_id:
        products = Product.query.filter_by(categoryId=category_id).all()
    else:
        products = Product.query.all()
    categories = Category.query.all()
    # Simulated AI recommendations (just random 3 for demo)
    import random
    recommendations = random.sample(products, min(3, len(products))) if products else []
    return render_template('index.html', products=products, categories=categories, recommendations=recommendations)

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
            elif isinstance(user, Supplier):
                return redirect(url_for('supplier_dashboard'))
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
    if not isinstance(current_user, Student): return "Unauthorized", 403
    cart = current_user.manageCart()
    payment_method = request.form.get('payment_method', 'card')
    delivery_address = request.form.get('delivery_address', current_user.address)
    try:
        # Override address temporarily for this checkout
        original_address = current_user.address
        current_user.address = delivery_address
        order = current_user.placeOrder(cart)
        current_user.address = original_address # restore
        
        # Save payment method
        if order.payment:
            order.payment.method = payment_method
            db.session.commit()
            
        if payment_method == 'cod':
            order.updateStatus("Confirmed")
            Notification.sendNotification(order.studentId, "Order", f"Order #{order.orderId} confirmed via COD")
            flash("Order confirmed via Cash on Delivery!", "success")
            return redirect(url_for('order_confirmation', order_id=order.orderId))
            
        return redirect(url_for('payment', order_id=order.orderId))
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('cart'))


@app.route('/payment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def payment(order_id):
    order = db.get_or_404(Order, order_id)
    
    # Security: Verify this user owns the order
    if not isinstance(current_user, Student) or order.studentId != current_user.id:
        return "Unauthorized", 403
        
    if request.method == 'POST':
        action = request.form.get('action')
        success = (action == 'success')
        
        # Explicit mock payment
        order.payment.processPayment("DEMO_MOCK_PAYMENT", success=success)
        
        if success:
            order.updateStatus("Confirmed")
            Notification.sendNotification(order.studentId, "Order", f"Payment successful for Order #{order.orderId}")
            flash("[DEMO] Payment simulated successfully. Order confirmed!", "success")
            return redirect(url_for('order_confirmation', order_id=order.orderId))
        else:
            order.updateStatus("Payment Failed")
            flash("[DEMO] Payment simulation failed. Order remains unpaid.", "danger")
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
    from sqlalchemy import func
    
    total_sales = db.session.query(func.sum(Order.totalAmount)).filter(Order.status.in_(['Confirmed', 'Completed', 'Delivered'])).scalar() or 0.0
    pending_orders = Order.query.filter(Order.status == 'Pending').count()
    low_stock_items = Product.query.filter(Product.stockQuantity < 5).count()
    recent_orders = Order.query.order_by(Order.orderDate.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html', 
        total_sales=total_sales, 
        pending_orders=pending_orders, 
        low_stock_items=low_stock_items,
        recent_orders=recent_orders)

@app.route('/delivery')
@login_required
def delivery_dashboard():
    if not isinstance(current_user, DeliveryPartner):
        return "Unauthorized", 403
    deliveries = current_user.receiveDeliveryRequest()
    return render_template('delivery_dashboard.html', deliveries=deliveries)


@app.route('/admin/inventory', methods=['GET', 'POST'])
@login_required
def admin_inventory():
    if not isinstance(current_user, Admin):
        return "Unauthorized", 403
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        qty = int(request.form.get('quantity'))
        product = Product.query.get(product_id)
        if product:
            product.stockQuantity = qty
            if product.inventory:
                product.inventory.quantity = qty
            db.session.commit()
            flash('Inventory updated successfully.', 'success')
        return redirect(url_for('admin_inventory'))
    
    products = Product.query.all()
    return render_template('inventory.html', products=products)

@app.route('/supplier', methods=['GET', 'POST'])
@login_required
def supplier_dashboard():
    if not isinstance(current_user, Supplier):
        return "Unauthorized", 403
    
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        
        # Verify product belongs to supplier
        product = Product.query.filter_by(productId=product_id, supplierId=current_user.supplierId).first()
        if product:
            current_user.updateStock(product.productId, quantity)
            flash('Stock updated successfully', 'success')
        else:
            flash('Unauthorized or Invalid Product', 'danger')
        return redirect(url_for('supplier_dashboard'))

    # Only show supplier's own products
    products = Product.query.filter_by(supplierId=current_user.supplierId).all()
    return render_template('supplier_dashboard.html', products=products)

# Feature: Profile Editing
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        if name and phone:
            current_user.updateProfile(name, phone)
            flash('Profile updated successfully!', 'success')
        else:
            flash('Name and phone are required.', 'danger')
        return redirect(url_for('profile'))
    return render_template('profile.html')

# Feature: Notifications
@app.route('/notifications')
@login_required
def notifications():
    notifs = Notification.query.filter_by(userId=current_user.id).order_by(Notification.sentAt.desc()).all()
    return render_template('notifications.html', notifications=notifs)

# Feature: Admin Reports
@app.route('/admin/reports')
@login_required
def admin_reports():
    if not isinstance(current_user, Admin):
        return "Unauthorized", 403
    from sqlalchemy import func
    
    total_sales = db.session.query(func.sum(Order.totalAmount)).filter(Order.status.in_(['Confirmed', 'Completed', 'Delivered'])).scalar() or 0.0
    total_orders = Order.query.filter(Order.status == 'Confirmed').count()
    total_inventory = db.session.query(func.sum(Inventory.quantity)).scalar() or 0
    
    return render_template('reports.html', total_sales=total_sales, total_orders=total_orders, total_inventory=total_inventory)

# Feature: Order Receipt
@app.route('/order/receipt/<int:order_id>')
@login_required
def order_receipt(order_id):
    order = db.get_or_404(Order, order_id)
    if not isinstance(current_user, Admin) and order.studentId != current_user.id:
        return "Unauthorized", 403
    return render_template('receipt.html', order=order, invoice_text=order.generateOrder())

# Feature: Rate Delivery
@app.route('/delivery/rate/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def rate_delivery(delivery_id):
    if not isinstance(current_user, Student):
        return "Unauthorized", 403
    delivery = db.get_or_404(Delivery, delivery_id)
    if delivery.order.studentId != current_user.id:
        return "Unauthorized", 403
        
    # Prevent duplicate review
    existing_review = Review.query.filter_by(studentId=current_user.id, deliveryId=delivery_id).first()
    if existing_review:
        flash("You have already reviewed this delivery.", "warning")
        return redirect(url_for('orders'))
        
    if request.method == 'POST':
        rating = int(request.form.get('rating', 5))
        comment = request.form.get('comment', '')
        if 1 <= rating <= 5:
            current_user.rateDelivery(delivery_id, rating, comment)
            flash("Review submitted successfully!", "success")
            return redirect(url_for('orders'))
        else:
            flash("Rating must be between 1 and 5.", "danger")
    return render_template('rate_delivery.html', delivery=delivery)


# === PHASE 3: NEW ROUTES ===

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        roll_no = request.form.get('rollNo')
        hostel = request.form.get('hostel')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
            
        student = Student(name=name, email=email, phone=phone, password='tmp', rollNo=roll_no, hostel=hostel, address=hostel)
        student.register(password)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/cart/update/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    if not isinstance(current_user, Student): return "Unauthorized", 403
    quantity = int(request.form.get('quantity', 1))
    cart = current_user.manageCart()
    product = db.session.get(Product, product_id)
    if product and quantity > 0 and quantity <= product.stockQuantity:
        # Simple implementation: clear existing, add new. Or update.
        item = CartItem.query.filter_by(cartId=cart.cartId, productId=product_id).first()
        if item:
            item.quantity = quantity
            item.price = product.price
            db.session.commit()
            flash('Cart updated.', 'success')
        else:
            flash('Item not in cart.', 'danger')
    else:
        flash('Invalid quantity or out of stock.', 'danger')
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    if not isinstance(current_user, Student): return "Unauthorized", 403
    cart = current_user.manageCart()
    item = CartItem.query.filter_by(cartId=cart.cartId, productId=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Item removed from cart.', 'success')
    return redirect(url_for('cart'))

@app.route('/wishlist')
@login_required
def wishlist():
    if not isinstance(current_user, Student): return "Unauthorized", 403
    items = Wishlist.query.filter_by(studentId=current_user.id).all()
    return render_template('wishlist.html', items=items)

@app.route('/wishlist/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    if not isinstance(current_user, Student): return "Unauthorized", 403
    if not Wishlist.query.filter_by(studentId=current_user.id, productId=product_id).first():
        w = Wishlist(studentId=current_user.id, productId=product_id)
        db.session.add(w)
        db.session.commit()
        flash('Added to wishlist!', 'success')
    return redirect(request.referrer or url_for('index'))

@app.route('/wishlist/remove/<int:product_id>', methods=['POST'])
@login_required
def remove_from_wishlist(product_id):
    if not isinstance(current_user, Student): return "Unauthorized", 403
    w = Wishlist.query.filter_by(studentId=current_user.id, productId=product_id).first()
    if w:
        db.session.delete(w)
        db.session.commit()
        flash('Removed from wishlist.', 'success')
    return redirect(request.referrer or url_for('wishlist'))

@app.route('/groups')
@login_required
def groups():
    if not isinstance(current_user, Student): return "Unauthorized", 403
    all_groups = HostelGroup.query.all()
    my_groups = current_user.groups.all()
    return render_template('groups.html', all_groups=all_groups, my_groups=my_groups)

@app.route('/groups/join/<int:group_id>', methods=['POST'])
@login_required
def join_group(group_id):
    if not isinstance(current_user, Student): return "Unauthorized", 403
    group = db.session.get(HostelGroup, group_id)
    if group and group not in current_user.groups:
        current_user.groups.append(group)
        db.session.commit()
        flash(f'Joined {group.name} successfully!', 'success')
    return redirect(url_for('groups'))

@app.route('/delivery/update/<int:delivery_id>', methods=['POST'])
@login_required
def update_delivery(delivery_id):
    if not isinstance(current_user, DeliveryPartner): return "Unauthorized", 403
    d = db.session.get(Delivery, delivery_id)
    if d:
        new_status = request.form.get('status')
        if new_status in ['In Transit', 'Delivered']:
            d.status = new_status
            if new_status == 'Delivered':
                d.order.status = 'Delivered'
            db.session.commit()
            flash(f'Delivery status updated to {new_status}', 'success')
    return redirect(url_for('delivery_dashboard'))

@app.route('/admin/orders')
@login_required
def admin_orders():
    if not isinstance(current_user, Admin): return "Unauthorized", 403
    orders = Order.query.order_by(Order.orderDate.desc()).all()
    partners = DeliveryPartner.query.all()
    return render_template('admin_orders.html', orders=orders, partners=partners)

@app.route('/admin/orders/assign/<int:order_id>', methods=['POST'])
@login_required
def assign_delivery(order_id):
    if not isinstance(current_user, Admin): return "Unauthorized", 403
    order = db.session.get(Order, order_id)
    partner_id = request.form.get('partner_id')
    if order and order.delivery and partner_id:
        order.delivery.partnerId = partner_id
        db.session.commit()
        flash('Delivery partner assigned.', 'success')
    return redirect(url_for('admin_orders'))



@app.route('/admin/categories', methods=['GET', 'POST'])
@login_required
def admin_categories():
    if not isinstance(current_user, Admin): return "Unauthorized", 403
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if name:
            db.session.add(Category(name=name, description=description))
            db.session.commit()
            flash("Category created", "success")
        return redirect(url_for('admin_categories'))
    categories = Category.query.all()
    return render_template('admin_categories.html', categories=categories)

@app.route('/admin/products', methods=['GET', 'POST'])
@login_required
def admin_products():
    if not isinstance(current_user, Admin): return "Unauthorized", 403
    if request.method == 'POST':
        name = request.form.get('name')
        cat_id = request.form.get('category_id')
        price = float(request.form.get('price', 0.0))
        qty = int(request.form.get('quantity', 0))
        if name and cat_id:
            p = Product(categoryId=cat_id, supplierId=1, name=name, price=price, stockQuantity=qty, description="Added by admin")
            db.session.add(p)
            db.session.commit()
            flash("Product added", "success")
        return redirect(url_for('admin_products'))
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('admin_products.html', products=products, categories=categories)


@app.route('/order/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = db.get_or_404(Order, order_id)
    if not isinstance(current_user, Student) or order.studentId != current_user.id:
        return "Unauthorized", 403
    return render_template('confirmation.html', order=order)

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
