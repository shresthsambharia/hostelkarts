import os

files_to_fix = [
    r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\templates\cart.html",
    r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\templates\index.html",
    r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\templates\delivery_dashboard.html"
]

for file in files_to_fix:
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()

    # if missing endblock, append it
    if "{% endblock %}" not in text:
        text += "\n{% endblock %}"

    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)
