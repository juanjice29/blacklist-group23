import sys
import os

# Calculate the path to the root of the project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_jwt_extended import JWTManager
import pytest
from models import db as _db
from application import app


@pytest.fixture(scope="session")
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-secret"

    with app.app_context():
        _db.create_all()

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

    with app.app_context():
        _db.session.remove()
        _db.drop_all()
