import os

base_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\templates"
os.makedirs(base_dir, exist_ok=True)

def write_file(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

write_file("base.html", """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HostelKart</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">HostelKart</a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ms-auto">
                    {% if current_user.is_authenticated %}
                        <li class="nav-item"><a class="nav-link" href="#">{{ current_user.name }} ({{ current_user.type }})</a></li>
                        {% if current_user.type == 'student' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('cart') }}">Cart</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('orders') }}">Orders</a></li>
                        {% elif current_user.type == 'admin' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin_dashboard') }}">Admin Dashboard</a></li>
                        {% elif current_user.type == 'delivery_partner' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('delivery_dashboard') }}">Delivery Dashboard</a></li>
                        {% endif %}
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('logout') }}">Logout</a></li>
                    {% else %}
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('login') }}">Login</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>
    <div class="container mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
</body>
</html>
""")

write_file("index.html", """{% extends 'base.html' %}
{% block content %}
<h2>Products</h2>
<div class="row">
    {% for p in products %}
    <div class="col-md-4 mb-3">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">{{ p.name }}</h5>
                <p class="card-text">Price: ${{ p.price }}</p>
                <p class="card-text">Stock: {{ p.stockQuantity }}</p>
                <a href="{{ url_for('product_detail', product_id=p.productId) }}" class="btn btn-primary">View</a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
""")

write_file("login.html", """{% extends 'base.html' %}
{% block content %}
<h2>Login</h2>
<form method="POST">
    <div class="mb-3">
        <label>Email</label>
        <input type="email" name="email" class="form-control" required>
    </div>
    <div class="mb-3">
        <label>Password</label>
        <input type="password" name="password" class="form-control" required>
    </div>
    <button type="submit" class="btn btn-primary">Login</button>
</form>
{% endblock %}
""")

write_file("product_detail.html", """{% extends 'base.html' %}
{% block content %}
<h2>{{ product.name }}</h2>
<p>{{ product.description }}</p>
<p>Price: ${{ product.price }}</p>
<p>Available: {{ product.stockQuantity }}</p>

{% if current_user.is_authenticated and current_user.type == 'student' %}
    <form action="{{ url_for('add_to_cart', product_id=product.productId) }}" method="POST">
        <input type="number" name="quantity" value="1" min="1" max="{{ product.stockQuantity }}" class="form-control mb-2" style="width:100px;">
        <button type="submit" class="btn btn-success">Add to Cart</button>
    </form>
{% endif %}
{% endblock %}
""")

write_file("cart.html", """{% extends 'base.html' %}
{% block content %}
<h2>Your Cart</h2>
<table class="table">
    <thead><tr><th>Product</th><th>Price</th><th>Quantity</th><th>Subtotal</th></tr></thead>
    <tbody>
        {% for item in cart.items %}
        <tr>
            <td>{{ item.product.name }}</td>
            <td>${{ item.price }}</td>
            <td>{{ item.quantity }}</td>
            <td>${{ item.calculateSubtotal() }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
<h4>Total: ${{ cart.calculateTotal() }}</h4>
{% if cart.items %}
<form action="{{ url_for('checkout') }}" method="POST">
    <button type="submit" class="btn btn-primary">Proceed to Checkout</button>
</form>
{% endif %}
{% endblock %}
""")

write_file("checkout.html", """{% extends 'base.html' %}
{% block content %}
<h2>Payment for Order #{{ order.orderId }}</h2>
<p>Total Amount: ${{ order.totalAmount }}</p>
<form method="POST">
    <button type="submit" name="action" value="success" class="btn btn-success">Simulate Payment Success</button>
    <button type="submit" name="action" value="fail" class="btn btn-danger">Simulate Payment Fail</button>
</form>
{% endblock %}
""")

write_file("orders.html", """{% extends 'base.html' %}
{% block content %}
<h2>Your Orders</h2>
<table class="table">
    <thead><tr><th>Order ID</th><th>Date</th><th>Amount</th><th>Status</th></tr></thead>
    <tbody>
        {% for o in orders %}
        <tr>
            <td>{{ o.orderId }}</td>
            <td>{{ o.orderDate.strftime('%Y-%m-%d %H:%M') }}</td>
            <td>${{ o.totalAmount }}</td>
            <td>{{ o.status }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
""")

write_file("admin_dashboard.html", """{% extends 'base.html' %}
{% block content %}
<h2>Admin Dashboard</h2>
<p>Welcome, {{ current_user.name }}. You can manage the system here.</p>
<!-- Links to inventory, users, products management would go here -->
{% endblock %}
""")

write_file("delivery_dashboard.html", """{% extends 'base.html' %}
{% block content %}
<h2>Delivery Partner Dashboard</h2>
<table class="table">
    <thead><tr><th>Delivery ID</th><th>Order ID</th><th>Address</th><th>Status</th></tr></thead>
    <tbody>
        {% for d in deliveries %}
        <tr>
            <td>{{ d.deliveryId }}</td>
            <td>{{ d.orderId }}</td>
            <td>{{ d.deliveryAddress }}</td>
            <td>{{ d.status }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
""")

print("Frontend templates generated successfully.")
