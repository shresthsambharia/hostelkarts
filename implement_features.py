import os

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"

# 1. Update order.py (generateOrder)
order_file = os.path.join(app_dir, 'models', 'order.py')
with open(order_file, 'r', encoding='utf-8') as f:
    order_code = f.read()
order_code = order_code.replace(
    "def generateOrder(self):\n        # Implementation of generating invoice/details\n        pass",
    """def generateOrder(self):
        invoice_lines = [f"INVOICE FOR ORDER #{self.orderId}"]
        invoice_lines.append(f"Date: {self.orderDate.strftime('%Y-%m-%d %H:%M')}")
        invoice_lines.append(f"Status: {self.status}")
        invoice_lines.append("-----------------------------")
        for item in self.items:
            invoice_lines.append(f"- {item.product.name} (x{item.quantity}) @ ${item.price} = ${item.calculateSubtotal()}")
        invoice_lines.append("-----------------------------")
        invoice_lines.append(f"Total Amount: ${self.totalAmount}")
        return "\\n".join(invoice_lines)"""
)
with open(order_file, 'w', encoding='utf-8') as f:
    f.write(order_code)

# 2. Update notification.py (sendNotification)
notif_file = os.path.join(app_dir, 'models', 'notification.py')
with open(notif_file, 'r', encoding='utf-8') as f:
    notif_code = f.read()
notif_code = notif_code.replace(
    "def sendNotification(self):\n        # Implementation of push/email notification\n        pass",
    """@staticmethod
    def sendNotification(user_id, notif_type, message):
        n = Notification(userId=user_id, type=notif_type, message=message)
        db.session.add(n)
        db.session.commit()
        return n"""
)
with open(notif_file, 'w', encoding='utf-8') as f:
    f.write(notif_code)

# 3. Patch app.py to include new routes and features
app_file = os.path.join(app_dir, 'app.py')
with open(app_file, 'r', encoding='utf-8') as f:
    app_code = f.read()

new_routes = """
# Feature: Profile Editing
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        if name and phone:
            current_user.updateProfile(name, phone)
            flash('Profile updated successfully!', 'success')
        else:
            flash('Name and phone are required.', 'danger')
        return redirect(url_for('profile'))
    return render_template('profile.html')

# Feature: Notifications
@app.route('/notifications')
@login_required
def notifications():
    notifs = Notification.query.filter_by(userId=current_user.id).order_by(Notification.sentAt.desc()).all()
    return render_template('notifications.html', notifications=notifs)

# Feature: Admin Reports
@app.route('/admin/reports')
@login_required
def admin_reports():
    if not isinstance(current_user, Admin):
        return "Unauthorized", 403
    from sqlalchemy import func
    
    total_sales = db.session.query(func.sum(Order.totalAmount)).filter(Order.status == 'Confirmed').scalar() or 0.0
    total_orders = Order.query.filter(Order.status == 'Confirmed').count()
    total_inventory = db.session.query(func.sum(Inventory.quantity)).scalar() or 0
    
    return render_template('reports.html', total_sales=total_sales, total_orders=total_orders, total_inventory=total_inventory)

# Feature: Order Receipt
@app.route('/order/receipt/<int:order_id>')
@login_required
def order_receipt(order_id):
    order = Order.query.get_or_404(order_id)
    if not isinstance(current_user, Admin) and order.studentId != current_user.id:
        return "Unauthorized", 403
    return render_template('receipt.html', order=order, invoice_text=order.generateOrder())

# Feature: Rate Delivery
@app.route('/delivery/rate/<int:delivery_id>', methods=['GET', 'POST'])
@login_required
def rate_delivery(delivery_id):
    if not isinstance(current_user, Student):
        return "Unauthorized", 403
    delivery = Delivery.query.get_or_404(delivery_id)
    if delivery.order.studentId != current_user.id:
        return "Unauthorized", 403
        
    # Prevent duplicate review
    existing_review = Review.query.filter_by(studentId=current_user.id, deliveryId=delivery_id).first()
    if existing_review:
        flash("You have already reviewed this delivery.", "warning")
        return redirect(url_for('orders'))
        
    if request.method == 'POST':
        rating = int(request.form.get('rating', 5))
        comment = request.form.get('comment', '')
        if 1 <= rating <= 5:
            current_user.rateDelivery(delivery_id, rating, comment)
            flash("Review submitted successfully!", "success")
            return redirect(url_for('orders'))
        else:
            flash("Rating must be between 1 and 5.", "danger")
    return render_template('rate_delivery.html', delivery=delivery)
"""

if "@app.route('/profile')" not in app_code:
    app_code += new_routes
    
    # Also hook notifications into payment
    app_code = app_code.replace(
        """order.updateStatus("Confirmed")\n            flash("[DEMO] Payment simulated successfully. Order confirmed!", "success")""",
        """order.updateStatus("Confirmed")
            Notification.sendNotification(order.studentId, "Order", f"Payment successful for Order #{order.orderId}")
            flash("[DEMO] Payment simulated successfully. Order confirmed!", "success")"""
    )

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(app_code)

print("Backend patched for 5 new features.")
