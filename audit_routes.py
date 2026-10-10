import os

app_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\app.py"
with open(app_file, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update checkout
new_checkout = """@app.route('/checkout', methods=['POST'])
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
"""

import re
text = re.sub(r"@app\.route\('/checkout', methods=\['POST'\]\).*?return redirect\(url_for\('cart'\)\)", new_checkout, text, flags=re.DOTALL)

# 2. Add Confirmation Route
new_conf = """
@app.route('/order/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = db.get_or_404(Order, order_id)
    if not isinstance(current_user, Student) or order.studentId != current_user.id:
        return "Unauthorized", 403
    return render_template('confirmation.html', order=order)
"""
if "def order_confirmation" not in text:
    text = text.replace("def orders():", new_conf + "\n@app.route('/orders')\n@login_required\ndef orders():")

# 3. Update Payment Route success redirect to confirmation
text = text.replace("return redirect(url_for('orders'))", "return redirect(url_for('order_confirmation', order_id=order.orderId)) if success else redirect(url_for('orders'))")

# 4. Add Admin CRUD Routes (Products & Categories)
admin_crud = """
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
"""
if "def admin_categories():" not in text:
    # insert before app.run
    idx = text.rfind("if __name__ == '__main__':")
    text = text[:idx] + admin_crud + "\n" + text[idx:]

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(text)
print("Routes updated.")
