import pytest
from app import create_app
from app.db.models import db

# Fixture to create and return the app
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # for testing

    # Set up the database schema in memory
    with app.app_context():
        db.create_all()  # Create all the tables in the in-memory database
        yield app  # Yield the app instance to the test function

    # Clean up after the test
    with app.app_context():
        db.session.remove()  # Remove the session
        db.drop_all()  # Drop all tables after the test


# Fixture to create and return the test client
@pytest.fixture
def client(app):  # Use the app fixture to get the app
    return app.test_client()
