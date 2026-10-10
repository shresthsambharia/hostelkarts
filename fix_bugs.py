import os

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"
app_file = os.path.join(app_dir, 'app.py')

with open(app_file, 'r', encoding='utf-8') as f:
    app_lines = f.readlines()

# 1. Fix if __name__ == '__main__': blocking route registration
# Find where if __name__ is.
main_start_idx = -1
for i, line in enumerate(app_lines):
    if "if __name__ == '__main__':" in line:
        main_start_idx = i
        break

if main_start_idx != -1 and main_start_idx < len(app_lines) - 5:
    # There are routes after main!
    main_block = app_lines[main_start_idx:main_start_idx+3]
    app_lines = app_lines[:main_start_idx] + app_lines[main_start_idx+3:]
    # Put it at the very end
    app_lines.extend(['\n'] + main_block)
    
# 2. Fix .query.get in app.py
for i, line in enumerate(app_lines):
    if "User.query.get(int(user_id))" in line:
        app_lines[i] = line.replace("User.query.get(int(user_id))", "db.session.get(User, int(user_id))")
    if "Order.query.get_or_404(order_id)" in line:
        # get_or_404 is Flask-SQLAlchemy specific and still supported, but to be strictly modern we can keep it or change it to db.get_or_404
        app_lines[i] = line.replace("Order.query.get_or_404(order_id)", "db.get_or_404(Order, order_id)")
    if "Delivery.query.get_or_404(delivery_id)" in line:
        app_lines[i] = line.replace("Delivery.query.get_or_404(delivery_id)", "db.get_or_404(Delivery, delivery_id)")
        
with open(app_file, 'w', encoding='utf-8') as f:
    f.writelines(app_lines)

# 3. Fix demo_oop.py missing table
demo_file = os.path.join(app_dir, 'demo_oop.py')
with open(demo_file, 'r', encoding='utf-8') as f:
    demo_code = f.read()

demo_code = demo_code.replace("with app.app_context():", "with app.app_context():\n        from app import setup_database\n        setup_database()")
demo_code = demo_code.replace("Product.query.get(product.productId)", "db.session.get(Product, product.productId)")
with open(demo_file, 'w', encoding='utf-8') as f:
    f.write(demo_code)

# 4. Fix order_service.py query.get
order_svc_file = os.path.join(app_dir, 'services', 'order_service.py')
with open(order_svc_file, 'r', encoding='utf-8') as f:
    order_svc_code = f.read()

order_svc_code = order_svc_code.replace("Product.query.with_for_update().get(c_item.productId)", "db.session.get(Product, c_item.productId, with_for_update=True)")

with open(order_svc_file, 'w', encoding='utf-8') as f:
    f.write(order_svc_code)

print("Applied urgent bug fixes.")
