import os

file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\templates\index.html"
with open(file, 'r', encoding='utf-8') as f:
    text = f.read()

# Clean up trailing garbage and append endblock
text = text.replace("{% endif %}{ %   e n d b l o c k   % }", "{% endif %}")
text = text.replace("{% endif %} ÿþ{% endblock %}", "{% endif %}")
if "{% endblock %}" not in text:
    text += "\n{% endblock %}"

with open(file, 'w', encoding='utf-8') as f:
    f.write(text)
