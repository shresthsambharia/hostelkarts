import os

app_path = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\app.py"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix seed data for supplier
old_sup_seed = """sup = Supplier(name="Campus Store", phone="9988776655")
            db.session.add(sup)
            db.session.commit()"""

new_sup_seed = """if not Supplier.query.filter_by(email='supplier@hostelkart.com').first():
                sup = Supplier(name="Campus Store", email="supplier@hostelkart.com", phone="9988776655", supplierId=1)
                sup.register("supplier123")
            else:
                sup = Supplier.query.filter_by(email='supplier@hostelkart.com').first()"""

content = content.replace(old_sup_seed, new_sup_seed)

# Ensure login route handles supplier redirect
if "elif isinstance(user, Supplier):" not in content:
    login_replace = """elif isinstance(user, DeliveryPartner):
                return redirect(url_for('delivery_dashboard'))"""
    login_new = """elif isinstance(user, DeliveryPartner):
                return redirect(url_for('delivery_dashboard'))
            elif isinstance(user, Supplier):
                return redirect(url_for('supplier_dashboard'))"""
    content = content.replace(login_replace, login_new)

# Add supplier dashboard route
if "@app.route('/supplier')" not in content:
    supplier_routes = """
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
"""
    content = content + supplier_routes

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)

print("app.py patched.")
