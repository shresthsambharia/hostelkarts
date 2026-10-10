import os
os.environ['TESTING'] = '1'
import pytest
from app import app, db
from models import User, Student, Product, Category

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        with app.app_context():
            db.drop_all()

def test_inheritance(client):
    s = Student(name="Test", email="test@test.com", phone="123", password="123", rollNo="111")
    assert isinstance(s, User)
    assert isinstance(s, Student)
