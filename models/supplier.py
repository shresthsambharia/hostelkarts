from database import db
from models.user import User

class Supplier(User):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    supplierId = db.Column(db.Integer, unique=True)
    # name and phone are inherited from User

    __mapper_args__ = {
        'polymorphic_identity': 'supplier',
    }

    products = db.relationship('Product', backref='supplier', lazy=True)

    def supplyProducts(self, product, quantity):
        product.stockQuantity += quantity
        if product.inventory:
            product.inventory.quantity += quantity
        db.session.commit()

    def updateStock(self, productId, quantity):
        from models.inventory import Inventory
        inv = Inventory.query.filter_by(productId=productId).first()
        if inv:
            inv.updateStock(quantity)
