import os
import glob

templates_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\templates"
for filepath in glob.glob(os.path.join(templates_dir, "*.html")):
    if filepath.endswith("base.html"): continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if "{% endblock %}" not in text:
        text += "\n{% endblock %}"
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
