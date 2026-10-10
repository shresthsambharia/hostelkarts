import os

e2e_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\e2e_test.py"
with open(e2e_file, 'r', encoding='utf-8') as f:
    text = f.read()

if "'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'" not in text:
    text = text.replace("app.config['TESTING'] = True", "app.config['TESTING'] = True\n    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'")
    with open(e2e_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed e2e_test.py to use in-memory DB.")
