import os

file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\e2e_test.py"
with open(file, 'r', encoding='utf-8') as f:
    text = f.read()

# Add authenticated GET / check
auth_index_test = """
            # Test Authenticated Homepage
            client.post('/login', data={'email': 'student@hostelkart.com', 'password': 'student123'}, follow_redirects=True)
            r = client.get('/')
            assert r.status_code == 200, "Authenticated homepage failed to render"
            assert b"student@hostelkart.com" in r.data or b"John Doe" in r.data or b"Logout" in r.data
            print("Authenticated Homepage PASSED")
            """

text = text.replace("print(\"--- STARTING E2E BROWSER SIMULATION ---\")", "print(\"--- STARTING E2E BROWSER SIMULATION ---\")\n" + auth_index_test)

with open(file, 'w', encoding='utf-8') as f:
    f.write(text)
