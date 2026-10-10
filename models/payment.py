from database import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'
    paymentId = db.Column(db.Integer, primary_key=True)
    orderId = db.Column(db.Integer, db.ForeignKey('orders.orderId'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Pending')
    transactionId = db.Column(db.String(100), unique=True, nullable=True)

    def processPayment(self, method_name, success=True):
        import uuid
        self.method = method_name
        if success:
            self.status = 'Success'
            self.transactionId = "TXN" + str(uuid.uuid4()).replace("-", "")[:10].upper()
        else:
            self.status = 'Failed'
        db.session.commit()
        return self.status == 'Success'

    def getPaymentStatus(self):
        return self.status
