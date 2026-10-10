import os

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"

# 1. Fix infinite loop risk in templates
templates_to_fix = [
    'templates/index.html',
    'templates/product_detail.html',
    'templates/cart.html'
]

for tpl in templates_to_fix:
    tpl_path = os.path.join(app_dir, tpl)
    with open(tpl_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace onerror="this.src=..." with onerror="this.onerror=null; this.src=..."
    if 'onerror="this.src=' in content:
        content = content.replace('onerror="this.src=', 'onerror="this.onerror=null; this.src=')
        with open(tpl_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed onerror in {tpl}")

# 2. Fix admin dashboard sales calculation
app_file = os.path.join(app_dir, 'app.py')
with open(app_file, 'r', encoding='utf-8') as f:
    app_code = f.read()

old_sales_calc = "total_sales = db.session.query(func.sum(Order.totalAmount)).filter(Order.status == 'Confirmed').scalar() or 0.0"
new_sales_calc = "total_sales = db.session.query(func.sum(Order.totalAmount)).filter(Order.status.in_(['Confirmed', 'Completed', 'Delivered'])).scalar() or 0.0"

if old_sales_calc in app_code:
    app_code = app_code.replace(old_sales_calc, new_sales_calc)
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(app_code)
    print("Fixed total_sales calculation in app.py")

# 3. Check reports sales calculation too
old_sales_calc_reports = "total_sales = db.session.query(func.sum(Order.totalAmount)).filter(Order.status == 'Confirmed').scalar() or 0.0"
if old_sales_calc_reports in app_code:
    app_code = app_code.replace(old_sales_calc_reports, new_sales_calc)
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(app_code)
    print("Fixed total_sales calculation for reports in app.py")

