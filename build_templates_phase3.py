import os

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"
templates_dir = os.path.join(app_dir, 'templates')

def write_tpl(name, content):
    with open(os.path.join(templates_dir, name), 'w', encoding='utf-8') as f:
        f.write(content.strip())

# 1. Update index.html (Categories & AI Recommender & Wishlist button)
index_file = os.path.join(templates_dir, 'index.html')
with open(index_file, 'r', encoding='utf-8') as f:
    index = f.read()

# Inject categories and AI Recs
cat_html = """
<div class="mb-4 d-flex gap-2 overflow-auto py-2">
    <a href="{{ url_for('index') }}" class="btn btn-outline-primary rounded-pill {% if not request.args.get('category_id') %}active{% endif %}">All</a>
    {% for c in categories %}
    <a href="{{ url_for('index', category_id=c.categoryId) }}" class="btn btn-outline-primary rounded-pill {% if request.args.get('category_id')|string == c.categoryId|string %}active{% endif %}">{{ c.name }}</a>
    {% endfor %}
</div>

{% if recommendations and not request.args.get('category_id') %}
<div class="mb-5 bg-light p-4 rounded-4 border border-primary border-opacity-25">
    <h4 class="fw-bold mb-3"><i class="bi bi-stars text-accent me-2"></i>AI Recommendations For You</h4>
    <div class="row g-3">
        {% for p in recommendations %}
        <div class="col-12 col-md-4">
            <div class="card h-100 border-0 shadow-sm">
                <div class="card-body d-flex align-items-center gap-3">
                    <img src="{{ url_for('static', filename='images/product_' ~ p.productId ~ '.svg') }}" onerror="this.onerror=null; this.src='{{ url_for('static', filename='images/fallback.svg') }}'" width="60" height="60" class="rounded object-fit-cover">
                    <div>
                        <h6 class="mb-1 fw-bold">{{ p.name }}</h6>
                        <a href="{{ url_for('product_detail', product_id=p.productId) }}" class="btn btn-sm btn-primary">View</a>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endif %}
"""
if "AI Recommendations" not in index:
    index = index.replace('<div class="d-flex justify-content-between align-items-end mb-4"', cat_html + '\n<div class="d-flex justify-content-between align-items-end mb-4"')
    
    # Add Wishlist icon on product cards
    wl_btn = """
    <form action="{{ url_for('add_to_wishlist', product_id=p.productId) }}" method="POST" class="d-inline position-absolute top-0 end-0 m-2 z-1">
        <button type="submit" class="btn btn-light rounded-circle shadow-sm p-2" title="Add to Wishlist"><i class="bi bi-heart text-danger"></i></button>
    </form>
    """
    index = index.replace('<div class="product-img-wrapper border-bottom">', wl_btn + '<div class="product-img-wrapper border-bottom">')
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index)

# 2. Update cart.html to support update/remove
cart_file = os.path.join(templates_dir, 'cart.html')
with open(cart_file, 'r', encoding='utf-8') as f:
    cart = f.read()

new_cart_qty = """
<form action="{{ url_for('update_cart', product_id=item.product.productId) }}" method="POST" class="d-flex align-items-center justify-content-center gap-1">
    <input type="number" name="quantity" value="{{ item.quantity }}" min="1" max="{{ item.product.stockQuantity }}" class="form-control form-control-sm text-center" style="width:60px;">
    <button type="submit" class="btn btn-sm btn-light border"><i class="bi bi-check2"></i></button>
</form>
"""
new_cart_subtotal = """
<td class="text-end align-middle fw-bold">
    ${{ "%.2f"|format(item.calculateSubtotal()) }}
    <form action="{{ url_for('remove_from_cart', product_id=item.product.productId) }}" method="POST" class="d-inline ms-2">
        <button type="submit" class="btn btn-sm btn-danger"><i class="bi bi-trash"></i></button>
    </form>
</td>
"""
if "update_cart" not in cart:
    cart = cart.replace('<span class="badge bg-light text-dark border">{{ item.quantity }}</span>', new_cart_qty)
    cart = cart.replace('<td class="text-end align-middle fw-bold">${{ "%.2f"|format(item.calculateSubtotal()) }}</td>', new_cart_subtotal)
    with open(cart_file, 'w', encoding='utf-8') as f:
        f.write(cart)

# 3. Update checkout.html to have a payment method selector
checkout_file = os.path.join(templates_dir, 'checkout.html')
with open(checkout_file, 'r', encoding='utf-8') as f:
    checkout = f.read()

payment_sel = """
<div class="mb-4 text-start">
    <label class="form-label fw-bold">Select Payment Method</label>
    <select name="payment_method" class="form-select">
        <option value="card">Credit/Debit Card</option>
        <option value="upi">UPI / Wallet</option>
        <option value="cod">Cash on Delivery (COD)</option>
    </select>
</div>
<form method="POST" class="d-flex flex-column gap-3">
"""
if "payment_method" not in checkout:
    checkout = checkout.replace('<form method="POST" class="d-flex flex-column gap-3">', payment_sel)
    with open(checkout_file, 'w', encoding='utf-8') as f:
        f.write(checkout)

# 4. Create register.html
write_tpl('register.html', """
{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow-sm border-0 mt-5">
            <div class="card-body p-4 p-md-5">
                <h3 class="fw-bold mb-4">Create Account</h3>
                <form method="POST">
                    <div class="mb-3">
                        <label class="form-label">Full Name</label>
                        <input type="text" name="name" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" name="email" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Phone</label>
                        <input type="text" name="phone" class="form-control" required>
                    </div>
                    <div class="row g-2 mb-4">
                        <div class="col-6">
                            <label class="form-label">Roll No</label>
                            <input type="text" name="rollNo" class="form-control" required>
                        </div>
                        <div class="col-6">
                            <label class="form-label">Hostel</label>
                            <input type="text" name="hostel" class="form-control" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Register</button>
                </form>
                <div class="text-center mt-3">
                    <a href="{{ url_for('login') }}">Already have an account? Login</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# 5. Create wishlist.html
write_tpl('wishlist.html', """
{% extends 'base.html' %}
{% block content %}
<h2 class="fw-bold mb-4"><i class="bi bi-heart-fill text-danger me-2"></i>My Wishlist</h2>
{% if items %}
<div class="row g-4">
    {% for w in items %}
    <div class="col-md-4 col-lg-3">
        <div class="card h-100 shadow-sm border-0">
            <div class="product-img-wrapper">
                <img src="{{ url_for('static', filename='images/product_' ~ w.productId ~ '.svg') }}" onerror="this.onerror=null; this.src='{{ url_for('static', filename='images/fallback.svg') }}'">
            </div>
            <div class="card-body">
                <h6 class="fw-bold">{{ w.product.name }}</h6>
                <p class="text-accent fw-bold">${{ "%.2f"|format(w.product.price) }}</p>
                <div class="d-flex justify-content-between">
                    <a href="{{ url_for('product_detail', product_id=w.productId) }}" class="btn btn-sm btn-primary">View</a>
                    <form action="{{ url_for('remove_from_wishlist', product_id=w.productId) }}" method="POST">
                        <button type="submit" class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% else %}
<div class="empty-state bg-white rounded shadow-sm border">
    <i class="bi bi-heart text-muted"></i>
    <h4>Your wishlist is empty</h4>
    <a href="{{ url_for('index') }}" class="btn btn-primary mt-3">Browse Products</a>
</div>
{% endif %}
{% endblock %}
""")

# 6. Create groups.html
write_tpl('groups.html', """
{% extends 'base.html' %}
{% block content %}
<h2 class="fw-bold mb-4"><i class="bi bi-people-fill text-primary me-2"></i>Hostel Groups</h2>
<div class="row g-4">
    <div class="col-md-6">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-header bg-white fw-bold">My Groups</div>
            <div class="list-group list-group-flush">
                {% for g in my_groups %}
                <div class="list-group-item py-3">
                    <h6 class="fw-bold">{{ g.name }}</h6>
                    <p class="mb-0 text-muted small">{{ g.description }}</p>
                </div>
                {% else %}
                <div class="list-group-item text-muted py-4 text-center">You haven't joined any groups yet.</div>
                {% endfor %}
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card shadow-sm border-0 h-100">
            <div class="card-header bg-white fw-bold">Available Groups</div>
            <div class="list-group list-group-flush">
                {% for g in all_groups %}
                    {% if g not in my_groups %}
                    <div class="list-group-item py-3 d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="fw-bold mb-1">{{ g.name }}</h6>
                            <p class="mb-0 text-muted small">{{ g.description }}</p>
                        </div>
                        <form action="{{ url_for('join_group', group_id=g.groupId) }}" method="POST">
                            <button type="submit" class="btn btn-sm btn-outline-primary">Join</button>
                        </form>
                    </div>
                    {% endif %}
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# 7. Create admin_orders.html
write_tpl('admin_orders.html', """
{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="fw-bold mb-0">Order Management</h2>
    <a href="{{ url_for('admin_dashboard') }}" class="btn btn-outline-secondary btn-sm">Back</a>
</div>
<div class="table-container shadow-sm">
    <table class="table table-hover align-middle mb-0">
        <thead>
            <tr>
                <th>Order ID</th>
                <th>Student ID</th>
                <th>Date</th>
                <th>Status</th>
                <th>Assign Partner</th>
            </tr>
        </thead>
        <tbody>
            {% for o in orders %}
            <tr>
                <td class="fw-bold">#{{ o.orderId }}</td>
                <td>{{ o.studentId }}</td>
                <td class="small">{{ o.orderDate.strftime('%b %d, %H:%M') }}</td>
                <td><span class="badge bg-light text-dark border">{{ o.status }}</span></td>
                <td>
                    {% if o.status == 'Confirmed' %}
                    <form action="{{ url_for('assign_delivery', order_id=o.orderId) }}" method="POST" class="d-flex gap-2">
                        <select name="partner_id" class="form-select form-select-sm" required style="width:130px;">
                            <option value="">Select...</option>
                            {% for dp in partners %}
                            <option value="{{ dp.id }}">{{ dp.name }}</option>
                            {% endfor %}
                        </select>
                        <button type="submit" class="btn btn-sm btn-primary">Assign</button>
                    </form>
                    {% elif o.delivery and o.delivery.partnerId %}
                    <span class="small text-success"><i class="bi bi-check-circle me-1"></i>Assigned (ID: {{ o.delivery.partnerId }})</span>
                    {% else %}
                    <span class="small text-muted">-</span>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
""")

# 8. Fix Delivery Dashboard Update Route
delivery_file = os.path.join(templates_dir, 'delivery_dashboard.html')
with open(delivery_file, 'r', encoding='utf-8') as f:
    delivery = f.read()

# Replace dummy button with real form
new_delivery_form = """
<form method="POST" action="{{ url_for('update_delivery', delivery_id=d.deliveryId) }}">
    <div class="d-grid gap-2">
        {% if d.status == 'Pending' %}
        <button type="submit" name="status" value="In Transit" class="btn btn-outline-primary btn-sm"><i class="bi bi-truck me-1"></i>Start Delivery</button>
        {% elif d.status == 'In Transit' %}
        <button type="submit" name="status" value="Delivered" class="btn btn-success btn-sm"><i class="bi bi-check2-circle me-1"></i>Mark Delivered</button>
        {% else %}
        <button type="button" class="btn btn-light btn-sm" disabled><i class="bi bi-check-all me-1"></i>Completed</button>
        {% endif %}
    </div>
</form>
"""
if "update_delivery" not in delivery:
    delivery = delivery.replace('<form method="POST" action="#">\n                    <div class="d-grid gap-2">\n                        <button type="button" class="btn btn-outline-success btn-sm"><i class="bi bi-check2-circle me-1"></i>Mark Delivered (Demo)</button>\n                    </div>\n                </form>', new_delivery_form)
    with open(delivery_file, 'w', encoding='utf-8') as f:
        f.write(delivery)

print("Phase 3 templates generated successfully.")
