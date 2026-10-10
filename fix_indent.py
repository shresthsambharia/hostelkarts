import os

app_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\app.py"
with open(app_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "else:" in line and "sup = Supplier.query.filter_by(email='supplier@hostelkart.com').first()" in lines[i+1]:
        lines[i] = "        else:\n"

with open(app_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)
