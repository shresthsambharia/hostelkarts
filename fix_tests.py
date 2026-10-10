import os

test_path = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\tests\test_workflows.py"
with open(test_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("db.session.add(p)\n            inv = Inventory(productId=p.productId, quantity=5)",
                          "db.session.add(p)\n            db.session.flush()\n            inv = Inventory(productId=p.productId, quantity=5)")

with open(test_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Tests fixed.")
