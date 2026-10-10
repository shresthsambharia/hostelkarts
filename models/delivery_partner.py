from database import db
from .user import User

class DeliveryPartner(User):
    __tablename__ = 'delivery_partners'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    partnerId = db.Column(db.Integer, unique=True)
    vehicleNo = db.Column(db.String(20))
    availability = db.Column(db.Boolean, default=True)
    location = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'delivery_partner',
    }

    def receiveDeliveryRequest(self):
        from models.delivery import Delivery
        return Delivery.query.filter_by(partnerId=self.id, status='Assigned').all()

    def updateDeliveryStatus(self, deliveryId, status):
        from models.delivery import Delivery
        delivery = Delivery.query.get(deliveryId)
        if delivery and delivery.partnerId == self.id:
            delivery.updateStatus(status)
            return True
        return False

    def trackDelivery(self, deliveryId):
        from models.delivery import Delivery
        return Delivery.query.get(deliveryId)
