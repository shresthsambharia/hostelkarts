import os

base_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\templates\base.html"
with open(base_file, 'r', encoding='utf-8') as f:
    code = f.read()

# Add profile, notifications for everyone except maybe logout link area
code = code.replace(
    '<li class="nav-item"><a class="nav-link" href="#">{{ current_user.name }} ({{ current_user.type }})</a></li>',
    """<li class="nav-item"><a class="nav-link" href="{{ url_for('profile') }}">{{ current_user.name }} ({{ current_user.type|capitalize }})</a></li>
       <li class="nav-item"><a class="nav-link" href="{{ url_for('notifications') }}">Notifications</a></li>"""
)

# Admin Reports
code = code.replace(
    '<li class="nav-item"><a class="nav-link" href="{{ url_for(\'admin_dashboard\') }}">Admin Dashboard</a></li>',
    """<li class="nav-item"><a class="nav-link" href="{{ url_for('admin_dashboard') }}">Admin Dashboard</a></li>
       <li class="nav-item"><a class="nav-link" href="{{ url_for('admin_reports') }}">Reports</a></li>"""
)

with open(base_file, 'w', encoding='utf-8') as f:
    f.write(code)

# Add receipt button and review button to orders.html
orders_file = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\templates\orders.html"
with open(orders_file, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("<th>Status</th></tr></thead>", "<th>Status</th><th>Actions</th></tr></thead>")
code = code.replace("<td>{{ o.status }}</td>\n        </tr>",
"""<td>{{ o.status }}</td>
            <td>
                <a href="{{ url_for('order_receipt', order_id=o.orderId) }}" class="btn btn-sm btn-info">Receipt</a>
                {% if o.delivery %}
                <a href="{{ url_for('rate_delivery', delivery_id=o.delivery.deliveryId) }}" class="btn btn-sm btn-warning">Rate Delivery</a>
                {% endif %}
            </td>
        </tr>""")

with open(orders_file, 'w', encoding='utf-8') as f:
    f.write(code)

print("Base and orders updated.")
