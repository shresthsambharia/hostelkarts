from app import app, db
from models import Category, Product

with app.app_context():
    print('Total Products:', Product.query.count())
    for c in Category.query.all():
        print(f"- {c.name}: {len(c.products)} products")
