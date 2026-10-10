# UML Class Mapping

| UML Class | Python File | Attributes Implemented | Methods Implemented |
|---|---|---|---|
| User | `models/user.py` | id, name, email, phone, password | register(), login(), updateProfile(), searchProducts() |
| Student | `models/student.py` | rollNo, hostel, address | placeOrder(), manageCart(), trackOrder(), rateDelivery() |
| Admin | `models/admin.py` | adminId, role | manageProducts(), manageInventory(), manageOrders(), manageUsers(), viewReports() |
| DeliveryPartner | `models/delivery_partner.py` | partnerId, vehicleNo, availability, location | receiveDeliveryRequest(), updateDeliveryStatus(), trackDelivery() |
| Category | `models/category.py` | categoryId, name, description | getProducts() |
| Product | `models/product.py` | productId, name, description, price, stockQuantity | getDetails(), getAvailability() |
| Supplier | `models/supplier.py` | supplierId, name, phone | supplyProducts(), updateStock() |
| Cart | `models/cart.py` | cartId, studentId, totalAmount | addItem(), removeItem(), updateQuantity(), calculateTotal() |
| CartItem | `models/cart.py` | cartItemId, productId, quantity, price | calculateSubtotal() |
| Order | `models/order.py` | orderId, studentId, orderDate, status, totalAmount | validateOrder(), generateOrder(), cancelOrder(), updateStatus() |
| OrderItem | `models/order.py` | orderItemId, productId, quantity, price | calculateSubtotal() |
| Payment | `models/payment.py` | paymentId, orderId, amount, method, status, transactionId | processPayment(), getPaymentStatus() |
| Inventory | `models/inventory.py` | inventoryId, productId, quantity, lastUpdated | checkAvailability(), updateStock() |
| Delivery | `models/delivery.py` | deliveryId, orderId, partnerId, status, deliveryAddress, assignedAt | assignPartner(), trackDelivery(), updateStatus() |
| Review | `models/review.py` | reviewId, studentId, productId, rating, comment | |
| Notification | `models/notification.py` | notificationId, userId, type, message, sentAt | sendNotification() |

## Text-Based Class Hierarchy
User (Base)
├── Student
├── Admin
├── DeliveryPartner
└── Supplier

## Sequence-Workflow Explanation
1. **Search & Cart**: Student accesses `/product/<id>`, adds to cart via `add_to_cart()`. Product availability is checked. `CartItem` created.
2. **Order**: Cart checkout calls `OrderService.create_order_from_cart`. Validates stock, locks prices, deducts inventory.
3. **Delivery**: Order creates a `Delivery`. Delivery partner updates status in `/delivery`.
4. **Supplier Inventory**: Suppliers log in and update their own stock via `/supplier`.
