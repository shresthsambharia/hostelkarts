import os

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"

# 1. Update style.css
css_file = os.path.join(app_dir, 'static', 'css', 'style.css')
with open(css_file, 'r', encoding='utf-8') as f:
    css = f.read()

new_css = """
/* Product Images */
.product-img-wrapper {
    position: relative;
    width: 100%;
    padding-top: 75%; /* 4:3 Aspect Ratio */
    background-color: #f8fafc;
    overflow: hidden;
}
.product-img-wrapper img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}
.card-hover:hover .product-img-wrapper img {
    transform: scale(1.05);
}
.product-detail-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    min-height: 400px;
}
"""
if ".product-img-wrapper" not in css:
    css += new_css
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css)

# 2. Update index.html
index_file = os.path.join(app_dir, 'templates', 'index.html')
with open(index_file, 'r', encoding='utf-8') as f:
    index = f.read()

# Replace product card top section
old_card_top = """<div class="card-body d-flex flex-column">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <span class="badge {% if p.stockQuantity > 0 %}bg-success-subtle text-success{% else %}bg-danger-subtle text-danger{% endif %} mb-2">
                        {% if p.stockQuantity > 0 %}<i class="bi bi-check2-circle me-1"></i> In Stock{% else %}<i class="bi bi-x-circle me-1"></i> Out of Stock{% endif %}
                    </span>
                    <h5 class="fw-bold text-accent mb-0">${{ "%.2f"|format(p.price) }}</h5>
                </div>"""

new_card_top = """<div class="product-img-wrapper border-bottom">
                <img src="{{ url_for('static', filename='images/product_' ~ p.productId ~ '.svg') }}" onerror="this.src='{{ url_for('static', filename='images/fallback.svg') }}'" alt="{{ p.name }}">
            </div>
            <div class="card-body d-flex flex-column pt-4">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <span class="badge {% if p.stockQuantity > 0 %}bg-success-subtle text-success{% else %}bg-danger-subtle text-danger{% endif %} mb-2">
                        {% if p.stockQuantity > 0 %}<i class="bi bi-check2-circle me-1"></i> In Stock{% else %}<i class="bi bi-x-circle me-1"></i> Out of Stock{% endif %}
                    </span>
                    <h5 class="fw-bold text-accent mb-0">${{ "%.2f"|format(p.price) }}</h5>
                </div>"""
index = index.replace(old_card_top, new_card_top)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(index)

# 3. Update product_detail.html
pd_file = os.path.join(app_dir, 'templates', 'product_detail.html')
with open(pd_file, 'r', encoding='utf-8') as f:
    pd = f.read()

old_pd_img = """<div class="col-md-5 bg-light d-flex align-items-center justify-content-center p-5 border-end">
                    <i class="bi bi-image text-muted" style="font-size: 5rem; opacity: 0.2;"></i>
                </div>"""
new_pd_img = """<div class="col-md-5 bg-light p-0 overflow-hidden border-end">
                    <img src="{{ url_for('static', filename='images/product_' ~ product.productId ~ '.svg') }}" onerror="this.src='{{ url_for('static', filename='images/fallback.svg') }}'" alt="{{ product.name }}" class="product-detail-img">
                </div>"""
pd = pd.replace(old_pd_img, new_pd_img)

with open(pd_file, 'w', encoding='utf-8') as f:
    f.write(pd)

print("Images integrated into UI.")
