import os
import re

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"
app_file = os.path.join(app_dir, 'app.py')

with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update setup_database() to create all tables and seed groups
seed_logic = """
        if not HostelGroup.query.first():
            db.session.add(HostelGroup(name='Block A Freshers', description='Discussions for Block A'))
            db.session.add(HostelGroup(name='Late Night Snacking', description='Order together to save delivery fee'))
            db.session.commit()
"""
if "Block A Freshers" not in content:
    content = content.replace("db.create_all()", "db.create_all()" + seed_logic)


new_routes = """
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
"""

if "@app.route('/register'" not in content:
    # Insert routes just before the main block
    main_block_idx = content.find("if __name__ == '__main__':")
    content = content[:main_block_idx] + new_routes + "\n\n" + content[main_block_idx:]
    
    # Also fix index route to handle Category filtering and AI Recommendations (simulated)
    old_index = """def index():
    products = Product.query.all()
    return render_template('index.html', products=products)"""
    new_index = """def index():
    category_id = request.args.get('category_id')
    if category_id:
        products = Product.query.filter_by(categoryId=category_id).all()
    else:
        products = Product.query.all()
    categories = Category.query.all()
    # Simulated AI recommendations (just random 3 for demo)
    import random
    recommendations = random.sample(products, min(3, len(products))) if products else []
    return render_template('index.html', products=products, categories=categories, recommendations=recommendations)"""
    
    content = content.replace(old_index, new_index)
    
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Routes patched.")
else:
    print("Routes already present.")
