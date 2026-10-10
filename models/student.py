from database import db
from .user import User

class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    rollNo = db.Column(db.String(20), unique=True)
    hostel = db.Column(db.String(50))
    address = db.Column(db.String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def placeOrder(self, cart):
        from services.order_service import OrderService
        return OrderService.create_order_from_cart(self, cart)

    def manageCart(self):
        from models.cart import Cart
        cart = Cart.query.filter_by(studentId=self.id).first()
        if not cart:
            cart = Cart(studentId=self.id)
            db.session.add(cart)
            db.session.commit()
        return cart

    def trackOrder(self, orderId):
        from models.order import Order
        return Order.query.filter_by(orderId=orderId, studentId=self.id).first()

    def rateDelivery(self, deliveryId, rating, comment):
        from models.review import Review
        review = Review(studentId=self.id, deliveryId=deliveryId, rating=rating, comment=comment)
        db.session.add(review)
        db.session.commit()
        return review
