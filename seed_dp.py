import os

app_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\app.py"
with open(app_file, 'r', encoding='utf-8') as f:
    text = f.read()

seed_dp = """
        if not DeliveryPartner.query.filter_by(email='delivery@hostelkart.com').first():
            dp = DeliveryPartner(name='Delivery Boy', email='delivery@hostelkart.com', phone='555666777', password='tmp', partnerId='DP001', vehicleNo='XYZ-123')
            dp.register('delivery123')
"""
if "delivery@hostelkart.com" not in text:
    text = text.replace("if not Supplier.query.filter_by(email='supplier@hostelkart.com').first():", seed_dp + "\n        if not Supplier.query.filter_by(email='supplier@hostelkart.com').first():")
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Seeded Delivery Partner.")
