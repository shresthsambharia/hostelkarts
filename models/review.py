from database import db
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'reviews'
    reviewId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('products.productId'), nullable=True)
    deliveryId = db.Column(db.Integer, db.ForeignKey('deliveries.deliveryId'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
