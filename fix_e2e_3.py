import os

file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\e2e_test.py"
with open(file, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('description="Not Mine"', 'description="Fake description"')
text = text.replace('name="Not Mine", price=10, stockQuantity=10)', 'name="Not Mine", description="Fake description", price=10, stockQuantity=10)')

with open(file, 'w', encoding='utf-8') as f:
    f.write(text)
