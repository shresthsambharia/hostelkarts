import os

test_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\e2e_test.py"
with open(test_file, 'r', encoding='utf-8') as f:
    code = f.read()

new_tests = """
            # 6. Profile Editing
            client.get('/logout')
            client.post('/login', data={'email': 'student@hostelkart.com', 'password': 'student123'}, follow_redirects=True)
            r = client.post('/profile', data={'name': 'John Doe Edited', 'phone': '9998887776'}, follow_redirects=True)
            assert b"Profile updated successfully" in r.data
            assert b"John Doe Edited" in r.data
            print("Profile editing PASSED")
            
            # 7. Receipt Generation
            order = Order.query.first()
            r = client.get(f'/order/receipt/{order.orderId}')
            assert r.status_code == 200
            assert b"INVOICE FOR ORDER" in r.data
            print("Receipt Generation PASSED")
            
            # 8. Notifications
            r = client.get('/notifications')
            assert r.status_code == 200
            assert b"Payment successful" in r.data
            print("Notifications PASSED")
            
            # 9. Delivery Rating
            delivery = Delivery.query.first()
            r = client.post(f'/delivery/rate/{delivery.deliveryId}', data={'rating': 5, 'comment': 'Great!'}, follow_redirects=True)
            assert b"Review submitted successfully" in r.data
            
            # Try duplicate rating
            r = client.post(f'/delivery/rate/{delivery.deliveryId}', data={'rating': 4}, follow_redirects=True)
            assert b"already reviewed" in r.data
            print("Delivery Rating PASSED")
            
            # 10. Admin Reports
            client.get('/logout')
            client.post('/login', data={'email': 'admin@hostelkart.com', 'password': 'admin123'}, follow_redirects=True)
            r = client.get('/admin/reports')
            assert r.status_code == 200
            assert b"Total Sales" in r.data
            print("Admin Reports PASSED")
"""

# Insert right before the final print statement
code = code.replace("print(\"--- E2E SIMULATION COMPLETED SUCCESSFULLY ---\")", new_tests + "\n            print(\"--- E2E SIMULATION COMPLETED SUCCESSFULLY ---\")")

with open(test_file, 'w', encoding='utf-8') as f:
    f.write(code)

print("e2e_test patched.")
