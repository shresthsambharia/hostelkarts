from database import db

class Category(db.Model):
    __tablename__ = 'categories'
    categoryId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    products = db.relationship('Product', backref='category', lazy=True)

    def getProducts(self):
        return self.products
