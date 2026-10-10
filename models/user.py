from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def register(self, raw_password):
        self.password = generate_password_hash(raw_password)
        db.session.add(self)
        db.session.commit()

    def login(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def updateProfile(self, name, phone):
        self.name = name
        self.phone = phone
        db.session.commit()

    def searchProducts(self, query):
        from models.product import Product
        return Product.query.filter(Product.name.ilike(f'%{query}%')).all()
