from database import db
from datetime import datetime

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    orderItemId = db.Column(db.Integer, primary_key=True)
    orderId = db.Column(db.Integer, db.ForeignKey('orders.orderId'), nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('products.productId'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Immutable snapshot of price at order time

    product = db.relationship('Product')

    def calculateSubtotal(self):
        return self.quantity * self.price

class Order(db.Model):
    __tablename__ = 'orders'
    orderId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    orderDate = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="Pending")
    totalAmount = db.Column(db.Float, nullable=False)

    items = db.relationship('OrderItem', backref='order', lazy=True)
    payment = db.relationship('Payment', backref='order', uselist=False)
    delivery = db.relationship('Delivery', backref='order', uselist=False)

    def validateOrder(self):
        # Validation is usually done before creation, ensuring stock etc.
        return len(self.items) > 0

    def generateOrder(self):
        invoice_lines = [f"INVOICE FOR ORDER #{self.orderId}"]
        invoice_lines.append(f"Date: {self.orderDate.strftime('%Y-%m-%d %H:%M')}")
        invoice_lines.append(f"Status: {self.status}")
        invoice_lines.append("-----------------------------")
        for item in self.items:
            invoice_lines.append(f"- {item.product.name} (x{item.quantity}) @ ${item.price} = ${item.calculateSubtotal()}")
        invoice_lines.append("-----------------------------")
        invoice_lines.append(f"Total Amount: ${self.totalAmount}")
        return "\n".join(invoice_lines)

    def cancelOrder(self):
        if self.status in ['Pending', 'Confirmed', 'Payment Failed']:
            self.status = 'Cancelled'
            # Restore inventory
            for item in self.items:
                if item.product.inventory:
                    item.product.inventory.quantity += item.quantity
                item.product.stockQuantity += item.quantity
            db.session.commit()
            return True
        return False

    def updateStatus(self, new_status):
        self.status = new_status
        db.session.commit()
