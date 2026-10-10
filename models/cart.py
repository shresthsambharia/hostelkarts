from database import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    cartItemId = db.Column(db.Integer, primary_key=True)
    cartId = db.Column(db.Integer, db.ForeignKey('carts.cartId'), nullable=False)
    productId = db.Column(db.Integer, db.ForeignKey('products.productId'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)

    product = db.relationship('Product')

    def calculateSubtotal(self):
        return self.quantity * self.price

class Cart(db.Model):
    __tablename__ = 'carts'
    cartId = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    totalAmount = db.Column(db.Float, default=0.0)

    items = db.relationship('CartItem', backref='cart', lazy=True, cascade="all, delete-orphan")

    def addItem(self, product, quantity=1):
        item = CartItem.query.filter_by(cartId=self.cartId, productId=product.productId).first()
        if item:
            item.quantity += quantity
        else:
            item = CartItem(cartId=self.cartId, productId=product.productId, quantity=quantity, price=product.price)
            db.session.add(item)
        self.calculateTotal()
        db.session.commit()

    def removeItem(self, productId):
        item = CartItem.query.filter_by(cartId=self.cartId, productId=productId).first()
        if item:
            db.session.delete(item)
            self.calculateTotal()
            db.session.commit()

    def updateQuantity(self, productId, quantity):
        item = CartItem.query.filter_by(cartId=self.cartId, productId=productId).first()
        if item:
            item.quantity = quantity
            self.calculateTotal()
            db.session.commit()

    def calculateTotal(self):
        total = sum(item.calculateSubtotal() for item in self.items)
        self.totalAmount = total
        return total
