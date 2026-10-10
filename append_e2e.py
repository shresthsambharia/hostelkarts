import os

e2e_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\e2e_test.py"
with open(e2e_file, 'r', encoding='utf-8') as f:
    text = f.read()

new_tests = """
            # 11. Wishlist Workflow
            client.get('/logout')
            client.post('/login', data={'email': 'student@hostelkart.com', 'password': 'student123'}, follow_redirects=True)
            
            p2 = Product.query.first()
            r = client.post(f'/wishlist/add/{p2.productId}', follow_redirects=True)
            assert b"Added to wishlist" in r.data
            
            r = client.get('/wishlist')
            assert r.status_code == 200
            assert bytes(p2.name, 'utf-8') in r.data
            
            r = client.post(f'/wishlist/remove/{p2.productId}', follow_redirects=True)
            assert b"Removed from wishlist" in r.data
            print("Wishlist Workflow PASSED")
            
            # 12. Hostel Group Workflow
            r = client.get('/groups')
            assert b"Block A Freshers" in r.data
            
            group = HostelGroup.query.first()
            r = client.post(f'/groups/join/{group.groupId}', follow_redirects=True)
            assert b"Joined" in r.data
            print("Hostel Group Workflow PASSED")
            
            # 13. Category & Recommendations check
            r = client.get('/?category_id=1')
            assert r.status_code == 200
            
            r = client.get('/')
            assert b"AI Recommendations For You" in r.data
            print("Category & Recommendations PASSED")
            
            # 14. Admin Assign Delivery
            client.get('/logout')
            client.post('/login', data={'email': 'admin@hostelkart.com', 'password': 'admin123'}, follow_redirects=True)
            
            r = client.get('/admin/orders')
            assert r.status_code == 200
            
            order = Order.query.first()
            if order and order.delivery:
                dp = DeliveryPartner.query.first()
                r = client.post(f'/admin/orders/assign/{order.orderId}', data={'partner_id': dp.id}, follow_redirects=True)
                assert b"Assigned" in r.data or b"Delivery partner assigned" in r.data
            print("Admin Orders Workflow PASSED")
            
            # 15. Delivery Partner Actions
            client.get('/logout')
            client.post('/login', data={'email': 'delivery@hostelkart.com', 'password': 'delivery123'}, follow_redirects=True)
            
            if order and order.delivery:
                r = client.post(f'/delivery/update/{order.delivery.deliveryId}', data={'status': 'In Transit'}, follow_redirects=True)
                assert b"updated to In Transit" in r.data
            print("Delivery Partner Workflow PASSED")
"""

text = text.replace("print(\"--- E2E SIMULATION COMPLETED SUCCESSFULLY ---\")", new_tests + "\n            print(\"--- E2E SIMULATION COMPLETED SUCCESSFULLY ---\")")

with open(e2e_file, 'w', encoding='utf-8') as f:
    f.write(text)

print("E2E tests appended.")
