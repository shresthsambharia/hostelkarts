import os

app_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\app.py"
with open(app_file, 'r', encoding='utf-8') as f:
    text = f.read()

import re

# We will replace the entire setup_database function contents safely
new_setup = """def setup_database():
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
"""

# Replace from `def setup_database():` to `@app.route('/')`
text = re.sub(r"def setup_database\(\):.*?(?=@app\.route\('/'\))", new_setup + "\n", text, flags=re.DOTALL)

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(text)
