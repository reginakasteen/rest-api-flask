import os
import pytest
from app import create_app
from werkzeug.security import generate_password_hash

from app.db import User, Expense, db

@pytest.fixture(scope="module")
def test_client():
    os.environ["CONFIG_TYPE"] = "app.config.TestingConfig"
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def test_new_user():
    return User(username="user", password="1233445666")

@pytest.fixture(scope="module")
def init_db(test_client):
    db.create_all()
    default_user = User(
        username="dave",
        password=generate_password_hash("password123", method="pbkdf2")
    )
    second_user = User(
        username="fiona",
        password=generate_password_hash("password123", method="pbkdf2")
    )
    db.session.add_all([default_user, second_user])

    db.session.commit()

    expense = Expense(
        title="Title1",
        amount=100,
        user_id=default_user.id
    )
    expense1 = Expense(
        title="Title2",
        amount=30,
        user_id=default_user.id
    )
    expense2 = Expense(
        title="Title3",
        amount=888,
        user_id=default_user.id
    )

    db.session.add_all([expense, expense1, expense2])
    db.session.commit()

    yield

    db.drop_all()

@pytest.fixture(scope="module")
def default_user_token(test_client):
    response = test_client.post(
        "/users/login",
        json={
            "username": "dave",
            "password": "password123"
        }
    )

    yield response.json["access_token"]

@pytest.fixture(scope="module")
def second_user_token(test_client):
    response = test_client.post(
        "/users/login",
        json={
            "username": "fiona",
            "password": "password123"
        }
    )

    yield response.json["access_token"]