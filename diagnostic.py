from app import app, db
from models import Product

with app.app_context():
    print("Database URL:", db.engine.url)
    print("Product count in DB:", Product.query.count())
    
    # Run the exact query as index() route
    products = Product.query.all()
    print("Products returned by query:", len(products))
    print("First 10 distinct product names:", list(set([p.name for p in products]))[:10])

with app.test_client() as client:
    resp = client.get('/')
    html = resp.data.decode('utf-8')
    # Count how many times 'View Details' appears to count the cards
    card_count = html.count('View Details')
    print("Number of product cards in rendered HTML (Featured+Recommendations):", card_count)
    
    import re
    # Extract h5 tags inside the cards to get product names
    names = re.findall(r'<h5 class="fw-bold mb-2">(.*?)</h5>', html)
    print("Product names found in HTML:", list(set(names))[:10])
