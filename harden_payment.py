import os

app_path = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\app.py"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Make mock payment explicitly demo-only and enforce failure state
old_payment = """def payment(order_id):
    order = Order.query.get_or_404(order_id)
    if request.method == 'POST':
        action = request.form.get('action')
        success = (action == 'success')
        order.payment.processPayment("Credit Card Mock", success=success)
        if success:
            order.updateStatus("Confirmed")
            flash("Payment successful. Order placed!", "success")
        else:
            flash("Payment failed.", "danger")
        return redirect(url_for('orders'))
    return render_template('checkout.html', order=order)"""

new_payment = """def payment(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Security: Verify this user owns the order
    if not isinstance(current_user, Student) or order.studentId != current_user.id:
        return "Unauthorized", 403
        
    if request.method == 'POST':
        action = request.form.get('action')
        success = (action == 'success')
        
        # Explicit mock payment
        order.payment.processPayment("DEMO_MOCK_PAYMENT", success=success)
        
        if success:
            order.updateStatus("Confirmed")
            flash("[DEMO] Payment simulated successfully. Order confirmed!", "success")
        else:
            order.updateStatus("Payment Failed")
            flash("[DEMO] Payment simulation failed. Order remains unpaid.", "danger")
        return redirect(url_for('orders'))
    return render_template('checkout.html', order=order)"""

content = content.replace(old_payment, new_payment)

# Also update checkout.html to clarify demo
checkout_path = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python\templates\checkout.html"
new_checkout = """{% extends 'base.html' %}
{% block content %}
<h2>[DEMO MODE] Payment for Order #{{ order.orderId }}</h2>
<div class="alert alert-warning">
    <strong>Notice:</strong> This is a mock payment gateway for demonstration purposes only. Do not enter real payment details.
</div>
<p>Total Amount (Server Verified): ${{ order.totalAmount }}</p>
<form method="POST">
    <button type="submit" name="action" value="success" class="btn btn-success">Simulate Payment Success</button>
    <button type="submit" name="action" value="fail" class="btn btn-danger">Simulate Payment Fail</button>
</form>
{% endblock %}"""

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)

with open(checkout_path, "w", encoding="utf-8") as f:
    f.write(new_checkout)

print("Payment logic hardened.")
