from database import db

class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    wishlistId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('products.productId'), nullable=False)
    
    product = db.relationship('Product')