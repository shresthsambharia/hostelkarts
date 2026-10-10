import os

app_dir = r"C:\Users\user\.gemini\antigravity\scratch\HostelKart_Python"

# 1. New Models
wishlist_model = """
from database import db

class Wishlist(db.Model):
    __tablename__ = 'wishlists'
    wishlistId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('products.productId'), nullable=False)
    
    product = db.relationship('Product')
"""
with open(os.path.join(app_dir, 'models', 'wishlist.py'), 'w', encoding='utf-8') as f:
    f.write(wishlist_model.strip())

hostelgroup_model = """
from database import db

student_groups = db.Table('student_groups',
    db.Column('student_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('hostel_groups.groupId'), primary_key=True)
)

class HostelGroup(db.Model):
    __tablename__ = 'hostel_groups'
    groupId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    
    students = db.relationship('Student', secondary=student_groups, backref=db.backref('groups', lazy='dynamic'))
"""
with open(os.path.join(app_dir, 'models', 'hostel_group.py'), 'w', encoding='utf-8') as f:
    f.write(hostelgroup_model.strip())

# Update models/__init__.py
init_file = os.path.join(app_dir, 'models', '__init__.py')
with open(init_file, 'a', encoding='utf-8') as f:
    f.write("\nfrom .wishlist import Wishlist\nfrom .hostel_group import HostelGroup, student_groups\n")

print("Added Wishlist and HostelGroup models.")
