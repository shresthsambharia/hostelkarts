import os

file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\e2e_test.py"
with open(file, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('assert b"Supplier Dashboard" in r.data', 'assert b"Supplier Portal" in r.data')

with open(file, 'w', encoding='utf-8') as f:
    f.write(text)
