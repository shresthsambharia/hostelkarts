import os

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"
templates_dir = os.path.join(app_dir, 'templates')
static_css_dir = os.path.join(app_dir, 'static', 'css')

os.makedirs(static_css_dir, exist_ok=True)

# 1. CSS Design System
with open(os.path.join(static_css_dir, 'style.css'), 'w', encoding='utf-8') as f:
    f.write("""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --navy: #0f172a;
  --accent: #4f46e5;
  --accent-hover: #4338ca;
  --bg: #f8fafc;
  --text-main: #334155;
  --text-muted: #64748b;
  --radius: 16px;
  --radius-sm: 8px;
}

body {
  background-color: var(--bg);
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--text-main);
  -webkit-font-smoothing: antialiased;
}

/* Navbar */
.navbar {
  background-color: var(--navy) !important;
  padding: 1rem 0;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}
.navbar-brand {
  font-weight: 700;
  letter-spacing: -0.5px;
  font-size: 1.5rem;
}
.nav-link {
  font-weight: 500;
  transition: color 0.2s;
}

/* Cards */
.card {
  border-radius: var(--radius);
  border: none;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  overflow: hidden;
}
.card-hover:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
}
.card-header {
  background-color: transparent;
  border-bottom: 1px solid #f1f5f9;
  padding: 1.25rem 1.5rem;
  font-weight: 600;
}

/* Buttons */
.btn {
  border-radius: var(--radius-sm);
  font-weight: 500;
  padding: 0.5rem 1.25rem;
  transition: all 0.2s;
}
.btn-primary {
  background-color: var(--accent);
  border-color: var(--accent);
}
.btn-primary:hover {
  background-color: var(--accent-hover);
  border-color: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.3);
}

/* Forms */
.form-control, .form-select {
  border-radius: var(--radius-sm);
  border: 1px solid #cbd5e1;
  padding: 0.75rem 1rem;
}
.form-control:focus, .form-select:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 0.25rem rgba(79, 70, 229, 0.25);
}
label {
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: var(--text-main);
}

/* Hero */
.hero {
  background: linear-gradient(135deg, var(--navy) 0%, #1e293b 100%);
  color: white;
  padding: 4rem 2rem;
  border-radius: var(--radius);
  margin-bottom: 3rem;
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
  position: relative;
  overflow: hidden;
}
.hero h1 {
  font-weight: 700;
  letter-spacing: -1px;
}

/* Tables */
.table-container {
  background: white;
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
}
.table {
  margin-bottom: 0;
}
.table th {
  background-color: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
  color: var(--text-muted);
  font-weight: 600;
  padding: 1.25rem 1.5rem;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
}
.table td {
  padding: 1.25rem 1.5rem;
  vertical-align: middle;
  border-bottom: 1px solid #f1f5f9;
}

/* Badges */
.badge {
  border-radius: 6px;
  padding: 0.5em 0.75em;
  font-weight: 600;
}

/* Utilities */
.text-accent { color: var(--accent); }
.bg-navy { background-color: var(--navy); }
.empty-state { text-align: center; padding: 4rem 2rem; }
.empty-state i { font-size: 3rem; color: #cbd5e1; margin-bottom: 1rem; }
""")

# 2. Update Templates
def write_tpl(name, content):
    with open(os.path.join(templates_dir, name), 'w', encoding='utf-8') as f:
        f.write(content.strip())

# base.html
write_tpl('base.html', """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HostelKart | Premium Student Commerce</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark sticky-top">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center gap-2" href="{{ url_for('index') }}">
                <i class="bi bi-box-seam-fill text-accent" style="font-size: 1.5rem;"></i>
                HostelKart
            </a>
            <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto align-items-lg-center gap-2">
                    {% if current_user.is_authenticated %}
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle d-flex align-items-center gap-2" href="#" data-bs-toggle="dropdown">
                                <i class="bi bi-person-circle"></i>
                                {{ current_user.name }} ({{ current_user.type|capitalize }})
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end shadow border-0" style="border-radius: 12px;">
                                <li><a class="dropdown-item" href="{{ url_for('profile') }}"><i class="bi bi-person me-2"></i>Profile</a></li>
                                <li><a class="dropdown-item" href="{{ url_for('notifications') }}"><i class="bi bi-bell me-2"></i>Notifications</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item text-danger" href="{{ url_for('logout') }}"><i class="bi bi-box-arrow-right me-2"></i>Logout</a></li>
                            </ul>
                        </li>
                        
                        {% if current_user.type == 'student' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('orders') }}"><i class="bi bi-clock-history me-1"></i> Orders</a></li>
                            <li class="nav-item">
                                <a class="btn btn-light btn-sm ms-lg-2 fw-bold text-accent" href="{{ url_for('cart') }}">
                                    <i class="bi bi-cart3"></i> Cart
                                </a>
                            </li>
                        {% elif current_user.type == 'admin' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin_dashboard') }}"><i class="bi bi-speedometer2 me-1"></i> Dashboard</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin_inventory') }}"><i class="bi bi-boxes me-1"></i> Inventory</a></li>
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin_reports') }}"><i class="bi bi-graph-up me-1"></i> Reports</a></li>
                        {% elif current_user.type == 'delivery_partner' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('delivery_dashboard') }}"><i class="bi bi-truck me-1"></i> Deliveries</a></li>
                        {% elif current_user.type == 'supplier' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('supplier_dashboard') }}"><i class="bi bi-shop me-1"></i> Supplier Portal</a></li>
                        {% endif %}
                        
                    {% else %}
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('login') }}">Login</a></li>
                        <li class="nav-item"><a class="btn btn-primary btn-sm ms-lg-2" href="{{ url_for('login') }}">Get Started</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>
    
    <div class="container py-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            <div class="toast-container position-fixed bottom-0 end-0 p-3" style="z-index: 1080;">
                {% for category, message in messages %}
                <div class="toast show align-items-center text-bg-{{ category }} border-0 shadow-lg mb-2" role="alert" style="border-radius: 12px;">
                    <div class="d-flex">
                        <div class="toast-body fw-medium">
                            {% if category == 'success' %}<i class="bi bi-check-circle me-2"></i>
                            {% elif category == 'danger' %}<i class="bi bi-exclamation-triangle me-2"></i>
                            {% else %}<i class="bi bi-info-circle me-2"></i>{% endif %}
                            {{ message }}
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                    </div>
                </div>
                {% endfor %}
            </div>
          {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
    
    <footer class="text-center py-4 text-muted mt-5">
        <div class="container">
            <p class="mb-0">&copy; 2026 HostelKart. Premium Student Delivery.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Auto-hide toasts after 5 seconds
        document.addEventListener('DOMContentLoaded', function() {
            var toasts = document.querySelectorAll('.toast');
            toasts.forEach(function(toastNode) {
                setTimeout(function() {
                    var toast = new bootstrap.Toast(toastNode);
                    toast.hide();
                }, 5000);
            });
        });
    </script>
</body>
</html>
""")

# index.html
write_tpl('index.html', """
{% extends 'base.html' %}
{% block content %}
<div class="hero text-center text-md-start d-flex align-items-center justify-content-between flex-wrap gap-4">
    <div class="hero-content">
        <h1 class="display-4 fw-bold mb-3">Hostel Essentials, <br><span style="color: #818cf8;">Delivered Fast.</span></h1>
        <p class="lead mb-4 opacity-75" style="max-width: 500px;">Get snacks, stationery, and daily needs delivered directly to your hostel room. Secure, fast, and student-friendly.</p>
        <a href="#products" class="btn btn-light btn-lg text-navy fw-bold px-4 rounded-pill">Shop Now <i class="bi bi-arrow-right ms-2"></i></a>
    </div>
    <div class="hero-icon d-none d-lg-block opacity-50" style="font-size: 12rem; line-height: 1;">
        <i class="bi bi-box-seam"></i>
    </div>
</div>

<div class="d-flex justify-content-between align-items-end mb-4" id="products">
    <h3 class="fw-bold mb-0">Featured Products</h3>
</div>

{% if products %}
<div class="row g-4">
    {% for p in products %}
    <div class="col-12 col-sm-6 col-lg-4 col-xl-3">
        <div class="card card-hover h-100 d-flex flex-column">
            <div class="card-body d-flex flex-column">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <span class="badge {% if p.stockQuantity > 0 %}bg-success-subtle text-success{% else %}bg-danger-subtle text-danger{% endif %} mb-2">
                        {% if p.stockQuantity > 0 %}<i class="bi bi-check2-circle me-1"></i> In Stock{% else %}<i class="bi bi-x-circle me-1"></i> Out of Stock{% endif %}
                    </span>
                    <h5 class="fw-bold text-accent mb-0">${{ "%.2f"|format(p.price) }}</h5>
                </div>
                <h5 class="card-title fw-bold mb-2">{{ p.name }}</h5>
                <p class="card-text text-muted small flex-grow-1">{{ p.description|truncate(60) }}</p>
                <div class="mt-auto pt-3 border-top d-flex justify-content-between align-items-center">
                    <span class="small text-muted fw-medium">{{ p.stockQuantity }} left</span>
                    <a href="{{ url_for('product_detail', product_id=p.productId) }}" class="btn btn-outline-primary btn-sm rounded-pill px-3">View Details</a>
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% else %}
<div class="empty-state bg-white rounded shadow-sm">
    <i class="bi bi-search text-muted"></i>
    <h4>No products found</h4>
    <p class="text-muted">Check back later for new arrivals.</p>
</div>
{% endif %}
""")

# product_detail.html
write_tpl('product_detail.html', """
{% extends 'base.html' %}
{% block content %}
<div class="mb-4">
    <a href="{{ url_for('index') }}" class="text-decoration-none text-muted"><i class="bi bi-arrow-left me-2"></i>Back to Products</a>
</div>
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card shadow-sm border-0">
            <div class="row g-0">
                <div class="col-md-5 bg-light d-flex align-items-center justify-content-center p-5 border-end">
                    <i class="bi bi-image text-muted" style="font-size: 5rem; opacity: 0.2;"></i>
                </div>
                <div class="col-md-7">
                    <div class="card-body p-4 p-md-5 d-flex flex-column h-100">
                        <span class="badge {% if product.stockQuantity > 0 %}bg-success-subtle text-success{% else %}bg-danger-subtle text-danger{% endif %} align-self-start mb-3">
                            {% if product.stockQuantity > 0 %}{{ product.stockQuantity }} Available{% else %}Out of Stock{% endif %}
                        </span>
                        
                        <h2 class="fw-bold mb-2">{{ product.name }}</h2>
                        <h3 class="text-accent fw-bold mb-4">${{ "%.2f"|format(product.price) }}</h3>
                        
                        <p class="text-muted mb-4 flex-grow-1">{{ product.description }}</p>
                        
                        {% if current_user.is_authenticated and current_user.type == 'student' %}
                            {% if product.stockQuantity > 0 %}
                            <form action="{{ url_for('add_to_cart', product_id=product.productId) }}" method="POST" class="mt-auto border-top pt-4">
                                <div class="d-flex gap-3 align-items-center">
                                    <div class="input-group" style="width: 140px;">
                                        <span class="input-group-text bg-light">Qty</span>
                                        <input type="number" name="quantity" value="1" min="1" max="{{ product.stockQuantity }}" class="form-control text-center fw-bold">
                                    </div>
                                    <button type="submit" class="btn btn-primary flex-grow-1 py-2 shadow-sm">
                                        <i class="bi bi-cart-plus me-2"></i>Add to Cart
                                    </button>
                                </div>
                            </form>
                            {% else %}
                            <div class="alert alert-warning mt-auto mb-0"><i class="bi bi-exclamation-triangle me-2"></i> Currently out of stock.</div>
                            {% endif %}
                        {% elif not current_user.is_authenticated %}
                            <div class="mt-auto border-top pt-4">
                                <a href="{{ url_for('login') }}" class="btn btn-outline-primary w-100">Login to Purchase</a>
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""")

# cart.html
write_tpl('cart.html', """
{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="fw-bold mb-0">Your Shopping Cart</h2>
    <a href="{{ url_for('index') }}" class="btn btn-outline-secondary btn-sm">Continue Shopping</a>
</div>

{% if cart.items %}
<div class="row g-4">
    <div class="col-lg-8">
        <div class="table-container shadow-sm">
            <table class="table table-hover mb-0">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th class="text-center">Price</th>
                        <th class="text-center">Qty</th>
                        <th class="text-end">Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in cart.items %}
                    <tr>
                        <td>
                            <div class="d-flex align-items-center gap-3">
                                <div class="bg-light rounded p-2 text-center text-muted d-none d-sm-block" style="width: 48px; height: 48px;">
                                    <i class="bi bi-box"></i>
                                </div>
                                <div>
                                    <h6 class="mb-0 fw-bold">{{ item.product.name }}</h6>
                                </div>
                            </div>
                        </td>
                        <td class="text-center align-middle">${{ "%.2f"|format(item.price) }}</td>
                        <td class="text-center align-middle">
                            <span class="badge bg-light text-dark border">{{ item.quantity }}</span>
                        </td>
                        <td class="text-end align-middle fw-bold">${{ "%.2f"|format(item.calculateSubtotal()) }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
    
    <div class="col-lg-4">
        <div class="card shadow-sm border-0 sticky-top" style="top: 100px;">
            <div class="card-body p-4">
                <h5 class="fw-bold mb-4">Order Summary</h5>
                <div class="d-flex justify-content-between mb-3 text-muted">
                    <span>Subtotal</span>
                    <span>${{ "%.2f"|format(cart.calculateTotal()) }}</span>
                </div>
                <div class="d-flex justify-content-between mb-3 text-muted">
                    <span>Delivery Fee</span>
                    <span class="text-success">Free</span>
                </div>
                <hr>
                <div class="d-flex justify-content-between mb-4">
                    <span class="fw-bold fs-5">Total</span>
                    <span class="fw-bold fs-5 text-accent">${{ "%.2f"|format(cart.totalAmount) }}</span>
                </div>
                <form action="{{ url_for('checkout') }}" method="POST">
                    <button type="submit" class="btn btn-primary w-100 py-3 fw-bold shadow-sm">
                        Proceed to Checkout <i class="bi bi-shield-lock ms-2"></i>
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>
{% else %}
<div class="empty-state bg-white rounded shadow-sm border">
    <i class="bi bi-cart-x"></i>
    <h3 class="fw-bold">Your cart is empty</h3>
    <p class="text-muted mb-4">Looks like you haven't added anything to your cart yet.</p>
    <a href="{{ url_for('index') }}" class="btn btn-primary px-4 py-2">Start Shopping</a>
</div>
{% endif %}
""")

# checkout.html
write_tpl('checkout.html', """
{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-6 col-md-8">
        <div class="text-center mb-4">
            <h2 class="fw-bold text-danger"><i class="bi bi-shield-exclamation me-2"></i>DEMO MODE</h2>
            <p class="text-muted">Payment processing simulation</p>
        </div>
        
        <div class="card shadow-lg border-0 overflow-hidden">
            <div class="bg-warning text-dark text-center py-2 fw-bold px-3" style="font-size: 0.85rem; letter-spacing: 0.5px;">
                <i class="bi bi-info-circle me-1"></i> THIS IS A MOCK GATEWAY FOR DEMONSTRATION ONLY
            </div>
            <div class="card-body p-4 p-md-5">
                <div class="text-center mb-4 pb-4 border-bottom">
                    <h5 class="text-muted mb-1">Order #{{ order.orderId }} Total</h5>
                    <h1 class="fw-bold text-accent display-4">${{ "%.2f"|format(order.totalAmount) }}</h1>
                </div>
                
                <h6 class="fw-bold mb-3">Simulate Payment Result</h6>
                <p class="text-muted small mb-4">Choose an outcome below to test the transaction workflows and state transitions.</p>
                
                <form method="POST" class="d-flex flex-column gap-3">
                    <button type="submit" name="action" value="success" class="btn btn-success py-3 fw-bold d-flex align-items-center justify-content-center gap-2">
                        <i class="bi bi-check-circle-fill"></i> Simulate Payment Success
                    </button>
                    <button type="submit" name="action" value="fail" class="btn btn-outline-danger py-3 fw-bold d-flex align-items-center justify-content-center gap-2">
                        <i class="bi bi-x-circle-fill"></i> Simulate Payment Failure
                    </button>
                </form>
            </div>
            <div class="card-footer bg-light text-center py-3 text-muted small">
                No real card details are collected or processed.
            </div>
        </div>
    </div>
</div>
""")

# orders.html
write_tpl('orders.html', """
{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="fw-bold mb-0">Order History</h2>
</div>

{% if orders %}
<div class="table-container shadow-sm">
    <table class="table table-hover align-middle mb-0">
        <thead>
            <tr>
                <th>Order Details</th>
                <th>Date</th>
                <th>Total</th>
                <th>Status</th>
                <th class="text-end">Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for o in orders %}
            <tr>
                <td>
                    <span class="fw-bold text-navy">#{{ o.orderId }}</span>
                </td>
                <td>{{ o.orderDate.strftime('%b %d, %Y - %H:%M') }}</td>
                <td class="fw-bold">${{ "%.2f"|format(o.totalAmount) }}</td>
                <td>
                    {% if o.status == 'Pending' %} <span class="badge bg-warning text-dark"><i class="bi bi-hourglass me-1"></i>Pending</span>
                    {% elif o.status == 'Confirmed' %} <span class="badge bg-info text-dark"><i class="bi bi-check me-1"></i>Confirmed</span>
                    {% elif o.status == 'Completed' or o.status == 'Delivered' %} <span class="badge bg-success"><i class="bi bi-check2-all me-1"></i>{{ o.status }}</span>
                    {% elif o.status == 'Payment Failed' %} <span class="badge bg-danger"><i class="bi bi-credit-card-2-front me-1"></i>Payment Failed</span>
                    {% elif o.status == 'Cancelled' %} <span class="badge bg-secondary"><i class="bi bi-x me-1"></i>Cancelled</span>
                    {% else %} <span class="badge bg-light text-dark border">{{ o.status }}</span> {% endif %}
                </td>
                <td class="text-end">
                    <div class="btn-group btn-group-sm">
                        <a href="{{ url_for('order_receipt', order_id=o.orderId) }}" class="btn btn-outline-primary" title="View Receipt">
                            <i class="bi bi-receipt"></i> Receipt
                        </a>
                        {% if o.delivery and o.status in ['Completed', 'Delivered'] %}
                        <a href="{{ url_for('rate_delivery', delivery_id=o.delivery.deliveryId) }}" class="btn btn-outline-warning" title="Rate Delivery">
                            <i class="bi bi-star-fill"></i>
                        </a>
                        {% endif %}
                    </div>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% else %}
<div class="empty-state bg-white rounded shadow-sm border">
    <i class="bi bi-receipt"></i>
    <h3 class="fw-bold">No orders yet</h3>
    <p class="text-muted mb-4">You haven't placed any orders.</p>
    <a href="{{ url_for('index') }}" class="btn btn-primary px-4">Start Shopping</a>
</div>
{% endif %}
""")

# admin_dashboard.html
write_tpl('admin_dashboard.html', """
{% extends 'base.html' %}
{% block content %}
<div class="d-flex align-items-center mb-4 gap-3 border-bottom pb-3">
    <div class="bg-primary text-white rounded p-3 d-flex align-items-center justify-content-center" style="width: 50px; height: 50px;">
        <i class="bi bi-shield-lock-fill fs-4"></i>
    </div>
    <div>
        <h2 class="fw-bold mb-0">Admin Dashboard</h2>
        <p class="text-muted mb-0">System Overview & Management</p>
    </div>
</div>

<div class="row g-4 mb-4">
    <div class="col-md-4">
        <a href="{{ url_for('admin_inventory') }}" class="text-decoration-none">
            <div class="card card-hover h-100 bg-white border">
                <div class="card-body text-center p-4">
                    <i class="bi bi-boxes text-accent mb-3" style="font-size: 2.5rem;"></i>
                    <h5 class="fw-bold text-navy">Manage Inventory</h5>
                    <p class="text-muted small mb-0">Update stock and products</p>
                </div>
            </div>
        </a>
    </div>
    <div class="col-md-4">
        <a href="{{ url_for('admin_reports') }}" class="text-decoration-none">
            <div class="card card-hover h-100 bg-white border">
                <div class="card-body text-center p-4">
                    <i class="bi bi-graph-up text-success mb-3" style="font-size: 2.5rem;"></i>
                    <h5 class="fw-bold text-navy">View Reports</h5>
                    <p class="text-muted small mb-0">Sales and performance metrics</p>
                </div>
            </div>
        </a>
    </div>
</div>
{% endblock %}
""")

# delivery_dashboard.html
write_tpl('delivery_dashboard.html', """
{% extends 'base.html' %}
{% block content %}
<div class="d-flex align-items-center mb-4 gap-3 border-bottom pb-3">
    <div class="bg-warning text-dark rounded p-3 d-flex align-items-center justify-content-center" style="width: 50px; height: 50px;">
        <i class="bi bi-truck fs-4"></i>
    </div>
    <div>
        <h2 class="fw-bold mb-0">Delivery Operations</h2>
        <p class="text-muted mb-0">Partner ID: {{ current_user.partnerId }} | Vehicle: {{ current_user.vehicleNo }}</p>
    </div>
</div>

{% if deliveries %}
<div class="row g-4">
    {% for d in deliveries %}
    <div class="col-md-6 col-lg-4">
        <div class="card shadow-sm border-start border-4 border-warning h-100">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <span class="badge bg-light text-dark border">Delivery #{{ d.deliveryId }}</span>
                    <span class="badge bg-primary">{{ d.status }}</span>
                </div>
                <h5 class="fw-bold mb-1">Order #{{ d.orderId }}</h5>
                <p class="text-muted small mb-3"><i class="bi bi-geo-alt-fill text-danger me-1"></i> {{ d.deliveryAddress }}</p>
                
                <hr>
                <form method="POST" action="#">
                    <div class="d-grid gap-2">
                        <button type="button" class="btn btn-outline-success btn-sm"><i class="bi bi-check2-circle me-1"></i>Mark Delivered (Demo)</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% else %}
<div class="empty-state bg-white rounded shadow-sm border">
    <i class="bi bi-cup-hot text-muted"></i>
    <h3 class="fw-bold">No Active Deliveries</h3>
    <p class="text-muted">Take a break. New assignments will appear here.</p>
</div>
{% endif %}
{% endblock %}
""")

print("Finished writing Python generator script components.")
