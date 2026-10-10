import os

order_path = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\models\order.py"
with open(order_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "if self.status in ['Pending', 'Confirmed']:",
    "if self.status in ['Pending', 'Confirmed', 'Payment Failed']:"
)

with open(order_path, "w", encoding="utf-8") as f:
    f.write(content)

print("order.py patched to allow cancellation of failed orders.")
