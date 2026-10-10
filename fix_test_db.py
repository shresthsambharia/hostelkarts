import os

app_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\app.py"
with open(app_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Add a check for TESTING env var before db.init_app
if "os.environ.get('TESTING')" not in text:
    text = text.replace("app.config.from_object(Config)", "app.config.from_object(Config)\nimport os\nif os.environ.get('TESTING'):\n    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'")
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Patched app.py to respect TESTING env var.")

import glob
test_files = glob.glob(r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\tests\*.py")
for tf in test_files:
    with open(tf, 'r', encoding='utf-8') as f:
        tf_text = f.read()
    if "import os\nos.environ['TESTING'] = '1'" not in tf_text:
        tf_text = "import os\nos.environ['TESTING'] = '1'\n" + tf_text
        with open(tf, 'w', encoding='utf-8') as f:
            f.write(tf_text)
        print(f"Patched {os.path.basename(tf)}")

e2e_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\e2e_test.py"
with open(e2e_file, 'r', encoding='utf-8') as f:
    e2e_text = f.read()
if "import os\nos.environ['TESTING'] = '1'" not in e2e_text:
    e2e_text = "import os\nos.environ['TESTING'] = '1'\n" + e2e_text
    with open(e2e_file, 'w', encoding='utf-8') as f:
        f.write(e2e_text)
    print("Patched e2e_test.py")

