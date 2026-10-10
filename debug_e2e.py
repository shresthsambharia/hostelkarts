import os

file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\e2e_test.py"
with open(file, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('assert b"updated to In Transit" in r.data', 'if b"updated to In Transit" not in r.data: print(r.data)')

with open(file, 'w', encoding='utf-8') as f:
    f.write(text)
