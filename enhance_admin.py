import os

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"

# Update app.py admin dashboard route
app_file = os.path.join(app_dir, 'app.py')
with open(app_file, 'r', encoding='utf-8') as f:
    app_code = f.read()

old_admin_route = """@app.route('/admin')
@login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        return "Unauthorized", 403
    return render_template('admin_dashboard.html')"""

new_admin_route = """@app.route('/admin')
@login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        return "Unauthorized", 403
    from sqlalchemy import func
    
    total_sales = db.session.query(func.sum(Order.totalAmount)).filter(Order.status == 'Confirmed').scalar() or 0.0
    pending_orders = Order.query.filter(Order.status == 'Pending').count()
    low_stock_items = Product.query.filter(Product.stockQuantity < 5).count()
    recent_orders = Order.query.order_by(Order.orderDate.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html', 
        total_sales=total_sales, 
        pending_orders=pending_orders, 
        low_stock_items=low_stock_items,
        recent_orders=recent_orders)"""

if "low_stock_items" not in app_code:
    app_code = app_code.replace(old_admin_route, new_admin_route)
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(app_code)

# Update admin_dashboard.html
admin_dash_file = os.path.join(app_dir, 'templates', 'admin_dashboard.html')
new_admin_html = """{% extends 'base.html' %}
{% block content %}
<div class="d-flex align-items-center mb-4 gap-3 border-bottom pb-3">
    <div class="bg-primary text-white rounded p-3 d-flex align-items-center justify-content-center" style="width: 50px; height: 50px;">
        <i class="bi bi-shield-lock-fill fs-4"></i>
    </div>
    <div>
        <h2 class="fw-bold mb-0">Admin Overview</h2>
        <p class="text-muted mb-0">Monitor your store's real-time performance</p>
    </div>
</div>

<div class="row g-4 mb-5">
    <div class="col-md-4">
        <div class="card bg-white border h-100 shadow-sm border-start border-4 border-success">
            <div class="card-body p-4">
                <p class="text-uppercase text-muted fw-bold small mb-2">Confirmed Sales</p>
                <h2 class="fw-bold mb-0">${{ "%.2f"|format(total_sales) }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card bg-white border h-100 shadow-sm border-start border-4 border-warning">
            <div class="card-body p-4">
                <p class="text-uppercase text-muted fw-bold small mb-2">Pending Orders</p>
                <h2 class="fw-bold mb-0">{{ pending_orders }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card bg-white border h-100 shadow-sm border-start border-4 border-danger">
            <div class="card-body p-4">
                <p class="text-uppercase text-muted fw-bold small mb-2">Low Stock Alerts</p>
                <h2 class="fw-bold mb-0 text-danger">{{ low_stock_items }} <small class="text-muted fs-6 fw-normal">Items &lt; 5 qty</small></h2>
            </div>
        </div>
    </div>
</div>

<div class="row g-4">
    <div class="col-lg-8">
        <div class="card border shadow-sm">
            <div class="card-header bg-white border-bottom py-3 d-flex justify-content-between align-items-center">
                <h5 class="fw-bold mb-0"><i class="bi bi-clock-history me-2 text-accent"></i>Recent Orders</h5>
                <a href="{{ url_for('admin_reports') }}" class="btn btn-sm btn-outline-primary">Full Report</a>
            </div>
            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                    <thead class="bg-light">
                        <tr>
                            <th>Order ID</th>
                            <th>Date</th>
                            <th>Total</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for o in recent_orders %}
                        <tr>
                            <td class="fw-bold">#{{ o.orderId }}</td>
                            <td class="text-muted small">{{ o.orderDate.strftime('%b %d, %H:%M') }}</td>
                            <td class="fw-bold">${{ "%.2f"|format(o.totalAmount) }}</td>
                            <td>
                                {% if o.status == 'Pending' %} <span class="badge bg-warning text-dark">Pending</span>
                                {% elif o.status == 'Confirmed' %} <span class="badge bg-info text-dark">Confirmed</span>
                                {% elif o.status == 'Completed' %} <span class="badge bg-success">Completed</span>
                                {% elif o.status == 'Cancelled' %} <span class="badge bg-secondary">Cancelled</span>
                                {% else %} <span class="badge bg-light text-dark border">{{ o.status }}</span> {% endif %}
                            </td>
                        </tr>
                        {% else %}
                        <tr><td colspan="4" class="text-center text-muted py-4">No recent orders found in database.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <div class="col-lg-4">
        <div class="card border shadow-sm h-100">
            <div class="card-header bg-white border-bottom py-3">
                <h5 class="fw-bold mb-0"><i class="bi bi-gear-fill me-2 text-accent"></i>Quick Actions</h5>
            </div>
            <div class="list-group list-group-flush">
                <a href="{{ url_for('admin_inventory') }}" class="list-group-item list-group-item-action py-3 d-flex align-items-center gap-3">
                    <div class="bg-primary bg-opacity-10 text-primary rounded p-2"><i class="bi bi-boxes"></i></div>
                    <div>
                        <h6 class="mb-0 fw-bold">Manage Inventory</h6>
                        <small class="text-muted">Update product stock</small>
                    </div>
                </a>
                <a href="{{ url_for('admin_reports') }}" class="list-group-item list-group-item-action py-3 d-flex align-items-center gap-3">
                    <div class="bg-success bg-opacity-10 text-success rounded p-2"><i class="bi bi-bar-chart-fill"></i></div>
                    <div>
                        <h6 class="mb-0 fw-bold">Detailed Reports</h6>
                        <small class="text-muted">Global sales analytics</small>
                    </div>
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""

with open(admin_dash_file, 'w', encoding='utf-8') as f:
    f.write(new_admin_html)

print("Admin dashboard enriched.")
