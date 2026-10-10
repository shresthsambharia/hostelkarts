from database import db
from datetime import datetime

class Inventory(db.Model):
    __tablename__ = 'inventory'
    inventoryId = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, db.ForeignKey('products.productId'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def checkAvailability(self, req_qty):
        return self.quantity >= req_qty

    def updateStock(self, new_qty):
        if new_qty < 0:
            raise ValueError("Inventory cannot be negative")
        self.quantity = new_qty
        self.product.stockQuantity = new_qty
        db.session.commit()
