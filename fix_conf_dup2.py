import os
import re

app_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\app.py"
with open(app_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Strip all order_confirmation
text = re.sub(r"@app\.route\('/order/confirmation.*?\ndef order_confirmation.*?\n    return render_template\('confirmation\.html', order=order\)", "", text, flags=re.DOTALL)

# Re-insert at the bottom
new_conf = """
@app.route('/order/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = db.get_or_404(Order, order_id)
    if not isinstance(current_user, Student) or order.studentId != current_user.id:
        return "Unauthorized", 403
    return render_template('confirmation.html', order=order)
"""

idx = text.rfind("if __name__ == '__main__':")
text = text[:idx] + new_conf + "\n" + text[idx:]

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(text)
