import os

app_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\app.py"
with open(app_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "sup = Supplier(name=\"Campus Store\"" in line or "sup.register(\"supplier123\")" in line or "sup = Supplier.query.filter_by(email='supplier@hostelkart.com').first()" in line:
        lines[i] = "            " + line.strip() + "\n"
    elif "prod = Product(" in line or "inv = Inventory(" in line or "db.session.add(prod)" in line or "db.session.commit()" in line and i > 50 and i < 65:
        if "db.session.commit()" in line:
            lines[i] = "        " + line.strip() + "\n"
        else:
            lines[i] = "        " + line.strip() + "\n"
            
    if "db.session.add(inv)" in line and i < 65:
         lines[i] = "        " + line.strip() + "\n"

with open(app_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)
