import os

app_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\app.py"
with open(app_file, 'r', encoding='utf-8') as f:
    text = f.read()

import re
text = re.sub(r"(@app\.route\('/orders'\)\s*@login_required\s*)+def orders", r"@app.route('/orders')\n@login_required\ndef orders", text)

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(text)
