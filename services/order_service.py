from database import db
from models.order import Order, OrderItem
from models.payment import Payment
from models.inventory import Inventory
from models.product import Product
from models.delivery import Delivery

class OrderService:
    @staticmethod
    def create_order_from_cart(student, cart):
        if not cart.items:
            raise ValueError("Cart is empty")

        # Start transaction logically
        try:
            total = 0
            order = Order(studentId=student.id, totalAmount=0, status='Pending')
            db.session.add(order)
            db.session.flush() # Get orderId

            for c_item in cart.items:
                product = db.session.get(Product, c_item.productId, with_for_update=True)
                if not product or product.stockQuantity < c_item.quantity:
                    db.session.rollback()
                    raise ValueError(f"Not enough stock for {product.name if product else 'unknown product'}")
                
                # Update inventory
                product.stockQuantity -= c_item.quantity
                if product.inventory:
                    product.inventory.quantity -= c_item.quantity
                
                o_item = OrderItem(
                    orderId=order.orderId,
                    productId=product.productId,
                    quantity=c_item.quantity,
                    price=product.price # Price at order time snapshot
                )
                db.session.add(o_item)
                total += o_item.calculateSubtotal()
            
            order.totalAmount = total
            
            # Empty cart
            for c_item in cart.items:
                db.session.delete(c_item)
            cart.totalAmount = 0
            
            # Setup payment and delivery
            payment = Payment(orderId=order.orderId, amount=total)
            db.session.add(payment)
            
            delivery = Delivery(orderId=order.orderId, deliveryAddress=student.address)
            db.session.add(delivery)
            
            db.session.commit()
            return order
        except Exception as e:
            db.session.rollback()
            raise e
