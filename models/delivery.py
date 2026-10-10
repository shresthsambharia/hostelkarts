from database import db
from datetime import datetime

class Delivery(db.Model):
    __tablename__ = 'deliveries'
    deliveryId = db.Column(db.Integer, primary_key=True)
    orderId = db.Column(db.Integer, db.ForeignKey('orders.orderId'), nullable=False)
    partnerId = db.Column(db.Integer, db.ForeignKey('delivery_partners.id'), nullable=True)
    status = db.Column(db.String(50), default='Pending')
    deliveryAddress = db.Column(db.String(255), nullable=False)
    assignedAt = db.Column(db.DateTime, nullable=True)

    def assignPartner(self, partnerId):
        self.partnerId = partnerId
        self.status = 'Assigned'
        self.assignedAt = datetime.utcnow()
        db.session.commit()

    def trackDelivery(self):
        return self.status

    def updateStatus(self, new_status):
        self.status = new_status
        db.session.commit()
        
        # Consistent order update
        if self.order:
            if new_status == 'Delivered':
                self.order.updateStatus('Completed')
            else:
                self.order.updateStatus(new_status)
