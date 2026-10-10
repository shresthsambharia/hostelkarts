import os

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"
index_file = os.path.join(app_dir, 'templates', 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Strip all garbage from the end
text = text[:text.find("{% endif %}") + 11] + "\n{% endblock %}\n"

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(text)
