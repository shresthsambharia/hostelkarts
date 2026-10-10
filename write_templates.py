import os

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\templates"

def write_tpl(name, content):
    with open(os.path.join(app_dir, name), 'w', encoding='utf-8') as f:
        f.write(content)

write_tpl("profile.html", """{% extends 'base.html' %}
{% block content %}
<h2>Edit Profile</h2>
<form method="POST">
    <div class="mb-3">
        <label>Email (Unchangeable ID)</label>
        <input type="text" class="form-control" value="{{ current_user.email }}" disabled>
    </div>
    <div class="mb-3">
        <label>Role</label>
        <input type="text" class="form-control" value="{{ current_user.type|capitalize }}" disabled>
    </div>
    <div class="mb-3">
        <label>Name</label>
        <input type="text" name="name" class="form-control" value="{{ current_user.name }}" required>
    </div>
    <div class="mb-3">
        <label>Phone</label>
        <input type="text" name="phone" class="form-control" value="{{ current_user.phone }}" required>
    </div>
    <button type="submit" class="btn btn-primary">Update Profile</button>
</form>
{% endblock %}""")

write_tpl("notifications.html", """{% extends 'base.html' %}
{% block content %}
<h2>Notifications</h2>
{% if notifications %}
<ul class="list-group">
    {% for n in notifications %}
    <li class="list-group-item">
        <strong>[{{ n.type }}]</strong> {{ n.message }}
        <span class="text-muted float-end">{{ n.sentAt.strftime('%Y-%m-%d %H:%M') }}</span>
    </li>
    {% endfor %}
</ul>
{% else %}
<p>No notifications.</p>
{% endif %}
{% endblock %}""")

write_tpl("reports.html", """{% extends 'base.html' %}
{% block content %}
<h2>Admin Sales & Inventory Reports</h2>
<div class="row">
    <div class="col-md-4">
        <div class="card bg-success text-white">
            <div class="card-body">
                <h4>Total Sales</h4>
                <h2>${{ total_sales }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card bg-info text-white">
            <div class="card-body">
                <h4>Confirmed Orders</h4>
                <h2>{{ total_orders }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card bg-warning text-dark">
            <div class="card-body">
                <h4>Total Inventory Items</h4>
                <h2>{{ total_inventory }}</h2>
            </div>
        </div>
    </div>
</div>
{% endblock %}""")

write_tpl("receipt.html", """{% extends 'base.html' %}
{% block content %}
<h2>Order Receipt #{{ order.orderId }}</h2>
<div class="card">
    <div class="card-body">
        <pre>{{ invoice_text }}</pre>
    </div>
</div>
<a href="{{ url_for('orders') }}" class="btn btn-secondary mt-3">Back to Orders</a>
{% endblock %}""")

write_tpl("rate_delivery.html", """{% extends 'base.html' %}
{% block content %}
<h2>Rate Delivery (Order #{{ delivery.orderId }})</h2>
<form method="POST">
    <div class="mb-3">
        <label>Rating (1-5)</label>
        <input type="number" name="rating" min="1" max="5" value="5" class="form-control" required style="width:100px;">
    </div>
    <div class="mb-3">
        <label>Comment (Optional)</label>
        <textarea name="comment" class="form-control" rows="3"></textarea>
    </div>
    <button type="submit" class="btn btn-primary">Submit Review</button>
</form>
{% endblock %}""")

print("Templates generated.")
