import os

e2e_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\e2e_test.py"
with open(e2e_file, 'r', encoding='utf-8') as f:
    text = f.read()

new_tests = """
            # 16. Checkout with COD and Custom Address
            client.get('/logout')
            client.post('/login', data={'email': 'student@hostelkart.com', 'password': 'student123'})
            client.post(f'/add_to_cart/{p2.productId}')
            r = client.post('/checkout', data={'payment_method': 'cod', 'delivery_address': 'Room 999'}, follow_redirects=True)
            assert b"Order Confirmed!" in r.data
            
            # Check address saved logic indirectly or just confirm it works
            # 17. Admin CRUD Products and Categories
            client.get('/logout')
            client.post('/login', data={'email': 'admin@hostelkart.com', 'password': 'admin123'})
            r = client.post('/admin/categories', data={'name': 'NewCat', 'description': 'desc'}, follow_redirects=True)
            assert b"Category created" in r.data
            assert b"NewCat" in r.data
            
            r = client.post('/admin/products', data={'name': 'NewProd', 'category_id': 1, 'price': 9.99, 'quantity': 100}, follow_redirects=True)
            assert b"Product added" in r.data
            assert b"NewProd" in r.data
            print("Admin CRUD Workflow PASSED")
"""
text = text.replace('print("--- E2E SIMULATION COMPLETED SUCCESSFULLY ---")', new_tests + '\n            print("--- E2E SIMULATION COMPLETED SUCCESSFULLY ---")')

with open(e2e_file, 'w', encoding='utf-8') as f:
    f.write(text)
