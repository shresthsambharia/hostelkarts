import os

test_path = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\tests\test_workflows.py"
with open(test_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix student address in test fixture
content = content.replace('rollNo="111")', 'rollNo="111", address="123 Test St")')
content = content.replace('rollNo="S1")', 'rollNo="S1", address="Test")')
content = content.replace('rollNo="S2")', 'rollNo="S2", address="Test")')

# Fix supplier inventory test - make sure Inventory is created
old_sup_test = """p = Product(categoryId=cat.categoryId, supplierId=99, name="Supplier Product", price=15.0, stockQuantity=10)
        db.session.add(p)
        db.session.commit()
        
        # Test updateStock explicitly
        sup.updateStock(p.productId, 20)"""

new_sup_test = """p = Product(categoryId=cat.categoryId, supplierId=99, name="Supplier Product", price=15.0, stockQuantity=10)
        db.session.add(p)
        db.session.flush()
        inv = Inventory(productId=p.productId, quantity=10)
        db.session.add(inv)
        db.session.commit()
        
        # Test updateStock explicitly
        sup.updateStock(p.productId, 20)"""

content = content.replace(old_sup_test, new_sup_test)

with open(test_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Tests updated to fix fixture data.")
