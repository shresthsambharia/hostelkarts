import os
import glob
import re

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"
templates_dir = os.path.join(app_dir, 'templates')

for filepath in glob.glob(os.path.join(templates_dir, "*.html")):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Replace $ with ₹
    text = text.replace('$', '₹')
    
    # Fix the weird endblock in index.html
    if 'index.html' in filepath:
        text = re.sub(r'\{\s*%\s*e\s*n\s*d\s*b\s*l\s*o\s*c\s*k\s*%\s*\}', '', text)
        # ensure there's exactly one {% endblock %}
        text = text.replace("{% endblock %}\n{% endblock %}", "{% endblock %}")
        text = text.replace("{% endblock %} \n \n \n{% endblock %}", "{% endblock %}")
        text = text.replace("{% endblock %}\n \n \n{% endblock %}", "{% endblock %}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

# Also fix app.py if it has dollar signs in flash messages
app_file = os.path.join(app_dir, 'app.py')
with open(app_file, 'r', encoding='utf-8') as f:
    app_text = f.read()

app_text = app_text.replace('$', '₹')
with open(app_file, 'w', encoding='utf-8') as f:
    f.write(app_text)

print("Templates fixed.")
