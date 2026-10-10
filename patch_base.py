import os

base_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\templates\base.html"
with open(base_file, 'r', encoding='utf-8') as f:
    base = f.read()

# Add wishlist and groups for student
student_links = """<li class="nav-item"><a class="nav-link" href="{{ url_for('orders') }}"><i class="bi bi-clock-history me-1"></i> Orders</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('wishlist') }}"><i class="bi bi-heart me-1"></i> Wishlist</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('groups') }}"><i class="bi bi-people me-1"></i> Groups</a></li>"""

if "url_for('wishlist')" not in base:
    base = base.replace('<li class="nav-item"><a class="nav-link" href="{{ url_for(\'orders\') }}"><i class="bi bi-clock-history me-1"></i> Orders</a></li>', student_links)

# Add admin orders for admin
admin_links = """<li class="nav-item"><a class="nav-link" href="{{ url_for('admin_inventory') }}"><i class="bi bi-boxes me-1"></i> Inventory</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin_orders') }}"><i class="bi bi-box-seam me-1"></i> Orders</a></li>"""
if "url_for('admin_orders')" not in base:
    base = base.replace('<li class="nav-item"><a class="nav-link" href="{{ url_for(\'admin_inventory\') }}"><i class="bi bi-boxes me-1"></i> Inventory</a></li>', admin_links)

# Add register to not authenticated
not_auth_links = """<li class="nav-item"><a class="nav-link" href="{{ url_for('login') }}">Login</a></li>
                        <li class="nav-item"><a class="btn btn-primary btn-sm ms-lg-2" href="{{ url_for('register') }}">Register</a></li>"""
if "url_for('register')" not in base:
    base = base.replace('<li class="nav-item"><a class="nav-link" href="{{ url_for(\'login\') }}">Login</a></li>\n                        <li class="nav-item"><a class="btn btn-primary btn-sm ms-lg-2" href="{{ url_for(\'login\') }}">Get Started</a></li>', not_auth_links)

with open(base_file, 'w', encoding='utf-8') as f:
    f.write(base)

print("Base patched.")
