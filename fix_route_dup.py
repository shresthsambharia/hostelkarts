import os

app_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\app.py"
with open(app_file, 'r', encoding='utf-8') as f:
    text = f.read()

# We need to remove the duplicate order_confirmation blocks and just do it cleanly
import re
text = re.sub(r"@app\.route\('/order/confirmation.*?def order_confirmation.*?return render_template\('confirmation\.html', order=order\)", "", text, flags=re.DOTALL)

# Re-insert securely
new_conf = """
@app.route('/order/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = db.get_or_404(Order, order_id)
    if not isinstance(current_user, Student) or order.studentId != current_user.id:
        return "Unauthorized", 403
    return render_template('confirmation.html', order=order)
"""

text = text.replace("@app.route('/orders')\n@login_required\n@app.route('/orders')\n@login_required\ndef orders():", "@app.route('/orders')\n@login_required\ndef orders():")
text = text.replace("@app.route('/orders')\n@login_required\ndef orders():", new_conf + "\n@app.route('/orders')\n@login_required\ndef orders():", 1)

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(text)
