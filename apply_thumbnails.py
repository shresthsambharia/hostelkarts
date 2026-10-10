import os

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"

# 1. Update cart.html
cart_file = os.path.join(app_dir, 'templates', 'cart.html')
with open(cart_file, 'r', encoding='utf-8') as f:
    cart = f.read()

old_cart_img = """<div class="bg-light rounded p-2 text-center text-muted d-none d-sm-block" style="width: 48px; height: 48px;">
                                    <i class="bi bi-box"></i>
                                </div>"""
new_cart_img = """<div class="rounded overflow-hidden d-none d-sm-block border" style="width: 56px; height: 56px; flex-shrink: 0;">
                                    <img src="{{ url_for('static', filename='images/product_' ~ item.product.productId ~ '.svg') }}" onerror="this.src='{{ url_for('static', filename='images/fallback.svg') }}'" alt="{{ item.product.name }}" style="width:100%; height:100%; object-fit:cover;">
                                </div>"""
cart = cart.replace(old_cart_img, new_cart_img)

with open(cart_file, 'w', encoding='utf-8') as f:
    f.write(cart)

print("Cart updated.")
