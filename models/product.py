from database import db

class Product(db.Model):
    __tablename__ = 'products'
    productId = db.Column(db.Integer, primary_key=True)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.categoryId'), nullable=False)
    supplierId = db.Column(db.Integer, db.ForeignKey('suppliers.supplierId'), nullable=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stockQuantity = db.Column(db.Integer, default=0)

    inventory = db.relationship('Inventory', backref='product', uselist=False)

    def getDetails(self):
        return {
            'productId': self.productId,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stockQuantity': self.stockQuantity
        }

    def getAvailability(self):
        return self.stockQuantity > 0
