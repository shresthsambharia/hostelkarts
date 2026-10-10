import os

app_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\app.py"
with open(app_file, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("return redirect(url_for('order_confirmation', order_id=order.orderId)) if success else redirect(url_for('orders'))", "return redirect(url_for('orders'))")
text = text.replace("flash(\"[DEMO] Payment simulated successfully. Order confirmed!\", \"success\")\n        else:", "flash(\"[DEMO] Payment simulated successfully. Order confirmed!\", \"success\")\n            return redirect(url_for('order_confirmation', order_id=order.orderId))\n        else:")

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(text)
