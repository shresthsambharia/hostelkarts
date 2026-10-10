import os

templates_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\templates"

def w(name, c):
    with open(os.path.join(templates_dir, name), 'w', encoding='utf-8') as f:
        f.write(c.strip())

# 1. Update checkout.html for address
chk = os.path.join(templates_dir, 'checkout.html')
with open(chk, 'r', encoding='utf-8') as f:
    chk_text = f.read()

addr = """
<div class="mb-4 text-start">
    <label class="form-label fw-bold">Delivery Address</label>
    <textarea name="delivery_address" class="form-control" rows="2" required>{{ current_user.address }}</textarea>
</div>
"""
if "delivery_address" not in chk_text:
    chk_text = chk_text.replace('<div class="mb-4 text-start">\n    <label class="form-label fw-bold">Select Payment Method</label>', addr + '\n<div class="mb-4 text-start">\n    <label class="form-label fw-bold">Select Payment Method</label>')
    with open(chk, 'w', encoding='utf-8') as f:
        f.write(chk_text)

# 2. confirmation.html
w('confirmation.html', """
{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-6 text-center">
        <div class="card shadow-sm border-0 py-5 px-4" style="border-radius: 20px;">
            <i class="bi bi-check-circle-fill text-success mb-3" style="font-size: 5rem;"></i>
            <h2 class="fw-bold mb-3">Order Confirmed!</h2>
            <p class="text-muted mb-4">Your order #{{ order.orderId }} has been successfully placed and is being prepared.</p>
            <div class="d-flex gap-3 justify-content-center">
                <a href="{{ url_for('orders') }}" class="btn btn-primary px-4 rounded-pill">View Orders</a>
                <a href="{{ url_for('index') }}" class="btn btn-outline-secondary px-4 rounded-pill">Continue Shopping</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# 3. admin_categories.html
w('admin_categories.html', """
{% extends 'base.html' %}
{% block content %}
<h2 class="fw-bold mb-4">Manage Categories</h2>
<div class="row g-4">
    <div class="col-md-4">
        <div class="card shadow-sm border-0">
            <div class="card-body">
                <h5 class="fw-bold mb-3">Add Category</h5>
                <form method="POST">
                    <div class="mb-3">
                        <label>Name</label>
                        <input type="text" name="name" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label>Description</label>
                        <input type="text" name="description" class="form-control">
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Add</button>
                </form>
            </div>
        </div>
    </div>
    <div class="col-md-8">
        <div class="card shadow-sm border-0">
            <table class="table mb-0">
                <thead class="bg-light">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    {% for c in categories %}
                    <tr>
                        <td>{{ c.categoryId }}</td>
                        <td>{{ c.name }}</td>
                        <td>{{ c.description }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
""")

# 4. admin_products.html
w('admin_products.html', """
{% extends 'base.html' %}
{% block content %}
<h2 class="fw-bold mb-4">Manage Products</h2>
<div class="row g-4">
    <div class="col-md-4">
        <div class="card shadow-sm border-0">
            <div class="card-body">
                <h5 class="fw-bold mb-3">Add Product</h5>
                <form method="POST">
                    <div class="mb-3">
                        <label>Category</label>
                        <select name="category_id" class="form-select" required>
                            {% for c in categories %}
                            <option value="{{ c.categoryId }}">{{ c.name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="mb-3">
                        <label>Name</label>
                        <input type="text" name="name" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label>Price</label>
                        <input type="number" step="0.01" name="price" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label>Initial Stock</label>
                        <input type="number" name="quantity" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Add</button>
                </form>
            </div>
        </div>
    </div>
    <div class="col-md-8">
        <div class="card shadow-sm border-0">
            <table class="table mb-0">
                <thead class="bg-light">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Price</th>
                        <th>Stock</th>
                    </tr>
                </thead>
                <tbody>
                    {% for p in products %}
                    <tr>
                        <td>{{ p.productId }}</td>
                        <td>{{ p.name }}</td>
                        <td>${{ "%.2f"|format(p.price) }}</td>
                        <td>{{ p.stockQuantity }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
""")

print("Templates written.")
