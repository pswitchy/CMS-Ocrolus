import pytest
from app import create_app
from app.extensions import db

@pytest.fixture(scope='module')
def test_app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()