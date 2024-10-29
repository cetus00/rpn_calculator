import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError

from calculator.api.main import create_app
from calculator.db import db
from calculator.models import Stacks
from config import TestingConfig


@pytest.fixture(scope='session')
def app():
    # Create the Flask app with test configuration
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='session', autouse=True)
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def fill_db(app):
    """
    Fill test DB Stacks table with following test cases:
    - stack is empty
    - stack contains one element
    - stack contains two elements
    - stack contains 5 elements
    - stack's last element is 0
    """
    scopes = [Stacks(stack=[1]),Stacks(stack=[]),Stacks(stack=[0]),Stacks(stack=[1,0]),Stacks(stack=[1,0,-34,12,6])]
    for scope in scopes:
        db.session.add(scope)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    yield
    try:
        db.session.query(Stacks).delete()
        db.session.commit()
        db.session.execute(text("ALTER SEQUENCE stacks_id_seq RESTART WITH 1"))
        db.session.commit()
    except Exception:
        db.session.rollback()


@pytest.fixture
def runner(app):
    # Create a test runner for the Flask CLI
    return app.test_cli_runner()