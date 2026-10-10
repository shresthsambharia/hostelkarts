import os

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"
templates_dir = os.path.join(app_dir, 'templates')

def write_tpl(name, content):
    with open(os.path.join(templates_dir, name), 'w', encoding='utf-8') as f:
        f.write(content.strip())

# supplier_dashboard.html
write_tpl('supplier_dashboard.html', """
{% extends 'base.html' %}
{% block content %}
<div class="d-flex align-items-center mb-4 gap-3 border-bottom pb-3">
    <div class="bg-indigo text-white rounded p-3 d-flex align-items-center justify-content-center" style="width: 50px; height: 50px; background-color: #4f46e5;">
        <i class="bi bi-shop fs-4"></i>
    </div>
    <div>
        <h2 class="fw-bold mb-0">Supplier Portal</h2>
        <p class="text-muted mb-0">Manage your product availability</p>
    </div>
</div>

<div class="table-container shadow-sm">
    <table class="table table-hover align-middle mb-0">
        <thead>
            <tr>
                <th>Product Details</th>
                <th class="text-center">Current Stock</th>
                <th class="text-end">Update Inventory</th>
            </tr>
        </thead>
        <tbody>
            {% for p in products %}
            <tr>
                <td>
                    <h6 class="fw-bold mb-0 text-navy">{{ p.name }}</h6>
                    <small class="text-muted">ID: {{ p.productId }}</small>
                </td>
                <td class="text-center">
                    <span class="badge {% if p.stockQuantity > 10 %}bg-success-subtle text-success{% elif p.stockQuantity > 0 %}bg-warning-subtle text-warning{% else %}bg-danger-subtle text-danger{% endif %} border px-3 py-2 fs-6">
                        {{ p.stockQuantity }}
                    </span>
                </td>
                <td>
                    <form method="POST" class="d-flex justify-content-end gap-2">
                        <input type="hidden" name="product_id" value="{{ p.productId }}">
                        <input type="number" name="quantity" min="0" class="form-control" required style="width: 120px;" placeholder="New Stock">
                        <button type="submit" class="btn btn-primary"><i class="bi bi-arrow-repeat me-1"></i> Update</button>
                    </form>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="3" class="text-center py-4 text-muted">No products assigned to your supplier ID.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
""")

# inventory.html
write_tpl('inventory.html', """
{% extends 'base.html' %}
{% block content %}
<div class="mb-4 d-flex justify-content-between align-items-center border-bottom pb-3">
    <div>
        <h2 class="fw-bold mb-0">Admin Inventory Management</h2>
        <p class="text-muted mb-0">Central stock control</p>
    </div>
    <a href="{{ url_for('admin_dashboard') }}" class="btn btn-outline-secondary btn-sm"><i class="bi bi-arrow-left me-1"></i>Back</a>
</div>

<div class="table-container shadow-sm">
    <table class="table table-hover align-middle mb-0">
        <thead>
            <tr>
                <th>Product ID & Name</th>
                <th class="text-center">Global Stock</th>
                <th class="text-end">Manual Override</th>
            </tr>
        </thead>
        <tbody>
            {% for p in products %}
            <tr>
                <td>
                    <h6 class="fw-bold mb-0">{{ p.name }}</h6>
                    <small class="text-muted">ID: {{ p.productId }}</small>
                </td>
                <td class="text-center">
                    <span class="badge {% if p.stockQuantity > 0 %}bg-light text-dark{% else %}bg-danger text-white{% endif %} border fs-6">
                        {{ p.stockQuantity }}
                    </span>
                </td>
                <td>
                    <form method="POST" class="d-flex justify-content-end gap-2">
                        <input type="hidden" name="product_id" value="{{ p.productId }}">
                        <input type="number" name="quantity" value="{{ p.stockQuantity }}" min="0" class="form-control bg-light" style="width: 100px;">
                        <button type="submit" class="btn btn-primary btn-sm px-3">Set</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
""")

# login.html
write_tpl('login.html', """
{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center align-items-center" style="min-height: 70vh;">
    <div class="col-12 col-md-8 col-lg-5">
        <div class="card shadow-lg border-0 overflow-hidden" style="border-radius: 20px;">
            <div class="card-header text-center bg-navy text-white p-4 border-0">
                <i class="bi bi-box-seam-fill text-accent mb-2 d-inline-block" style="font-size: 2.5rem;"></i>
                <h3 class="fw-bold mb-0">Welcome Back</h3>
                <p class="text-white-50 small mb-0">Sign in to HostelKart</p>
            </div>
            <div class="card-body p-4 p-md-5">
                <form method="POST">
                    <div class="mb-4">
                        <label class="form-label text-muted small fw-bold text-uppercase">Email Address</label>
                        <div class="input-group">
                            <span class="input-group-text bg-light border-end-0 text-muted"><i class="bi bi-envelope"></i></span>
                            <input type="email" name="email" class="form-control border-start-0 ps-0 bg-light" required placeholder="student@hostelkart.com">
                        </div>
                    </div>
                    <div class="mb-4">
                        <label class="form-label text-muted small fw-bold text-uppercase">Password</label>
                        <div class="input-group">
                            <span class="input-group-text bg-light border-end-0 text-muted"><i class="bi bi-lock"></i></span>
                            <input type="password" name="password" class="form-control border-start-0 ps-0 bg-light" required placeholder="••••••••">
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary w-100 py-3 fw-bold shadow-sm">Secure Login</button>
                </form>
                
                <div class="mt-4 text-center">
                    <p class="text-muted small mb-1">Demo Accounts:</p>
                    <div class="d-flex flex-wrap justify-content-center gap-2 small">
                        <span class="badge bg-light text-dark border">student@hostelkart.com</span>
                        <span class="badge bg-light text-dark border">admin@hostelkart.com</span>
                        <span class="badge bg-light text-dark border">supplier@hostelkart.com</span>
                    </div>
                    <p class="text-muted small mt-2">Password: [role]123</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# profile.html
write_tpl('profile.html', """
{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-6">
        <h2 class="fw-bold mb-4">Account Settings</h2>
        <div class="card shadow-sm border-0">
            <div class="card-body p-4 p-md-5">
                <div class="d-flex align-items-center gap-3 mb-4 pb-4 border-bottom">
                    <div class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center" style="width: 64px; height: 64px; font-size: 1.5rem;">
                        {{ current_user.name[0]|upper }}
                    </div>
                    <div>
                        <h4 class="fw-bold mb-0">{{ current_user.name }}</h4>
                        <span class="badge bg-light text-dark border mt-1"><i class="bi bi-person-badge me-1"></i>{{ current_user.type|capitalize }}</span>
                    </div>
                </div>
                
                <form method="POST">
                    <div class="mb-4">
                        <label class="form-label text-muted small fw-bold text-uppercase">Email Address (Immutable ID)</label>
                        <input type="text" class="form-control bg-light" value="{{ current_user.email }}" disabled>
                        <div class="form-text"><i class="bi bi-info-circle me-1"></i> Email cannot be changed.</div>
                    </div>
                    <div class="row g-3 mb-4">
                        <div class="col-md-6">
                            <label class="form-label text-muted small fw-bold text-uppercase">Full Name</label>
                            <input type="text" name="name" class="form-control" value="{{ current_user.name }}" required>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label text-muted small fw-bold text-uppercase">Phone Number</label>
                            <input type="text" name="phone" class="form-control" value="{{ current_user.phone }}" required>
                        </div>
                    </div>
                    <div class="d-flex justify-content-end">
                        <button type="submit" class="btn btn-primary px-4 shadow-sm"><i class="bi bi-save me-2"></i>Save Changes</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# notifications.html
write_tpl('notifications.html', """
{% extends 'base.html' %}
{% block content %}
<h2 class="fw-bold mb-4">Notifications</h2>

<div class="row justify-content-center">
    <div class="col-lg-8">
        {% if notifications %}
        <div class="list-group shadow-sm border-0 rounded-4 overflow-hidden">
            {% for n in notifications %}
            <div class="list-group-item list-group-item-action p-4 border-start-0 border-end-0 border-bottom">
                <div class="d-flex gap-3">
                    <div class="mt-1">
                        {% if n.type == 'Order' %}
                        <i class="bi bi-box-seam text-primary fs-4"></i>
                        {% else %}
                        <i class="bi bi-bell text-secondary fs-4"></i>
                        {% endif %}
                    </div>
                    <div class="flex-grow-1">
                        <div class="d-flex justify-content-between align-items-center w-100 mb-1">
                            <h6 class="mb-0 fw-bold">{{ n.type }} Update</h6>
                            <small class="text-muted">{{ n.sentAt.strftime('%b %d, %H:%M') }}</small>
                        </div>
                        <p class="mb-0 text-muted">{{ n.message }}</p>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="empty-state bg-white rounded shadow-sm border">
            <i class="bi bi-bell-slash"></i>
            <h4 class="fw-bold">All caught up!</h4>
            <p class="text-muted">You have no new notifications.</p>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
""")

# reports.html
write_tpl('reports.html', """
{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center border-bottom pb-3 mb-4">
    <h2 class="fw-bold mb-0">Platform Analytics</h2>
    <a href="{{ url_for('admin_dashboard') }}" class="btn btn-outline-secondary btn-sm">Back</a>
</div>

<div class="row g-4">
    <div class="col-md-4">
        <div class="card shadow-sm border-0 h-100" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white;">
            <div class="card-body p-4">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <h6 class="text-white-50 text-uppercase fw-bold mb-0">Total Sales Vol.</h6>
                    <i class="bi bi-currency-dollar fs-4 opacity-50"></i>
                </div>
                <h1 class="display-5 fw-bold mb-0">${{ "%.2f"|format(total_sales) }}</h1>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card shadow-sm border-0 h-100" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white;">
            <div class="card-body p-4">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <h6 class="text-white-50 text-uppercase fw-bold mb-0">Confirmed Orders</h6>
                    <i class="bi bi-cart-check fs-4 opacity-50"></i>
                </div>
                <h1 class="display-5 fw-bold mb-0">{{ total_orders }}</h1>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card shadow-sm border-0 h-100 bg-white border">
            <div class="card-body p-4">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <h6 class="text-muted text-uppercase fw-bold mb-0">Global Inventory Items</h6>
                    <i class="bi bi-box-seam fs-4 text-muted opacity-50"></i>
                </div>
                <h1 class="display-5 fw-bold text-navy mb-0">{{ total_inventory }}</h1>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# receipt.html
write_tpl('receipt.html', """
{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex justify-content-between align-items-center mb-4 d-print-none">
            <h3 class="fw-bold mb-0">Digital Receipt</h3>
            <div>
                <button onclick="window.print()" class="btn btn-outline-primary btn-sm me-2"><i class="bi bi-printer me-1"></i>Print</button>
                <a href="{{ url_for('orders') }}" class="btn btn-secondary btn-sm">Close</a>
            </div>
        </div>
        
        <div class="card shadow-lg border-0 bg-white" style="border-top: 8px solid var(--navy) !important;">
            <div class="card-body p-5">
                <div class="text-center mb-5 pb-4 border-bottom">
                    <i class="bi bi-box-seam-fill text-accent mb-2" style="font-size: 2.5rem;"></i>
                    <h2 class="fw-bold text-navy mb-0">HOSTELKART</h2>
                    <p class="text-muted small text-uppercase letter-spacing-1">Official Tax Invoice</p>
                </div>
                <pre class="bg-light p-4 rounded text-dark fs-6" style="font-family: 'Courier New', Courier, monospace; border: 1px dashed #cbd5e1;">{{ invoice_text }}</pre>
                
                <div class="text-center mt-5 pt-4 border-top text-muted small">
                    <p class="mb-0">Thank you for shopping with HostelKart.</p>
                    <p>For support, contact support@hostelkart.com</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

# rate_delivery.html
write_tpl('rate_delivery.html', """
{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-6">
        <div class="card shadow-lg border-0 mt-4 overflow-hidden rounded-4">
            <div class="card-header bg-navy text-white text-center p-4 border-0">
                <h3 class="fw-bold mb-0">Rate Your Delivery</h3>
                <p class="text-white-50 small mb-0">Order #{{ delivery.orderId }}</p>
            </div>
            <div class="card-body p-4 p-md-5">
                <div class="text-center mb-4">
                    <i class="bi bi-truck text-accent" style="font-size: 3rem;"></i>
                    <h5 class="fw-bold mt-2 mb-0">How was your experience?</h5>
                </div>
                <form method="POST">
                    <div class="mb-4 text-center">
                        <label class="form-label text-muted small fw-bold text-uppercase">Rating (1-5)</label>
                        <input type="range" name="rating" min="1" max="5" value="5" class="form-range" id="ratingSlider" required>
                        <div class="d-flex justify-content-between px-2 text-muted small fw-bold">
                            <span>1 <i class="bi bi-star-fill text-warning"></i></span>
                            <span>3 <i class="bi bi-star-fill text-warning"></i></span>
                            <span>5 <i class="bi bi-star-fill text-warning"></i></span>
                        </div>
                    </div>
                    <div class="mb-4">
                        <label class="form-label text-muted small fw-bold text-uppercase">Feedback (Optional)</label>
                        <textarea name="comment" class="form-control bg-light" rows="3" placeholder="Tell us what you liked or what needs improvement..."></textarea>
                    </div>
                    <div class="d-flex justify-content-between gap-3">
                        <a href="{{ url_for('orders') }}" class="btn btn-light flex-grow-1">Cancel</a>
                        <button type="submit" class="btn btn-primary flex-grow-1 shadow-sm"><i class="bi bi-send me-2"></i>Submit Review</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""")

print("Finished writing Python generator script components 2.")
