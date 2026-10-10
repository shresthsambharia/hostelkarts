# HostelKart - Python OOP Mini Project

This is a fully functional web application developed with Python, Flask, and SQLite demonstrating Object-Oriented Programming principles and reproducing UML class and sequence diagrams.

## Features
- Complete UML class implementation with inheritance and associations.
- Role-based access for Students, Admins, and Delivery Partners.
- Shopping Cart and Checkout.
- Order management with price snapshots.
- Inventory tracking and validations.

## Setup Instructions
1. `python -m venv venv`
2. `venv\Scripts\activate` (Windows)
3. `pip install -r requirements.txt`
4. `python app.py`

## Demo Credentials
- Admin: admin@hostelkart.com / admin123
- Student: student@hostelkart.com / student123
- Delivery: partner@hostelkart.com / partner123

## Structure
- `models/`: Contains all UML mapped classes.
- `services/`: Contains business logic (e.g., placing orders, transaction handling).
- `templates/`: HTML views.
- `app.py`: Main Flask application.
