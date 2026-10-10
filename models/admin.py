from database import db
from .user import User

class Admin(User):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    adminId = db.Column(db.Integer, unique=True)
    role = db.Column(db.String(50), default="SuperAdmin")

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def manageProducts(self):
        from models.product import Product
        return Product.query.all()

    def manageInventory(self):
        from models.inventory import Inventory
        return Inventory.query.all()

    def manageOrders(self):
        from models.order import Order
        return Order.query.all()

    def manageUsers(self):
        return User.query.all()

    def viewReports(self):
        pass
