import pytest
from flask import url_for

from calculator.db import db
from calculator.models import Stacks


def test_get_all_stacks_stack(client, fill_db):
    response = client.get(url_for("rpn.stack.get_all_stacks"))
    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_create_new_stack(client, fill_db):
    # Example POST request to add to the stack in the test database
    response = client.post(url_for("rpn.stack.create_new_stack"))
    assert response.status_code == 200
    assert response.get_json()["id"] == 6
    new_stack = db.session.query(Stacks).filter(Stacks.id==6)
    assert new_stack

def test_get_stack(client, fill_db):
    response = client.get(url_for("rpn.stack.get_stack", stack_id=4))
    assert response.status_code == 200
    assert response.get_json()["stack"] == [1,0]

def test_add_good_value_to_stack(client, fill_db):
    stack_id = 1
    response = client.post(url_for("rpn.stack.add_value_to_stack", stack_id=stack_id), json={"value": 11})
    assert response.status_code == 204
    stack = db.session.query(Stacks.stack).filter(Stacks.id == stack_id).first()
    assert stack[0] == [1, 11]

def test_add_bad_value_to_stack(client, fill_db):
    response = client.post(url_for("rpn.stack.add_value_to_stack", stack_id=1), json={"value": "asda"})
    assert response.status_code == 400


def test_add_no_value_to_stack(client, fill_db):
    stack_id = 1
    response = client.post(url_for("rpn.stack.add_value_to_stack", stack_id=1), json={"message": "test"})
    assert response.status_code == 400
    stack = db.session.query(Stacks.stack).filter(Stacks.id == stack_id).first()
    assert stack[0] == [1]

def test_add_value_to_stack_stack_not_found(client, fill_db):
    response = client.post(url_for("rpn.stack.add_value_to_stack", stack_id=55), json={"value": 0})
    assert response.status_code == 404

def test_delete_existing_stack(client, fill_db):
    all_stacks = db.session.query(Stacks.stack).all()
    response = client.delete(url_for("rpn.stack.delete_stack", stack_id=2))
    assert response.status_code == 204
    new_all_stacks = db.session.query(Stacks.stack).all()
    assert len(new_all_stacks) == len(all_stacks) - 1


@pytest.mark.parametrize(
    "operand, stack_id, status_code, expected",
    [
        ("div", 5, 204, [1,0,-34,2]),
        ("div", 4, 422, [1,0]),
        ("add", 4, 204, [1]),
        ("add", 3, 422, [0]),
        ("sub", 5, 204, [1,0,-34,6]),
        ("mul", 5, 204, [1,0,-34,72]),
        ("qwerty", 5, 404, [1,0,-34,12,6]),
    ]
)
def test_apply_operand_to_stack(client, fill_db, operand, stack_id, status_code, expected):
    response = client.post(url_for("rpn.operand.apply_operand_to_stack", operand=operand, stack_id=stack_id))
    assert response.status_code == status_code
    stack = db.session.query(Stacks.stack).filter(Stacks.id == stack_id).first()
    assert stack[0] == expected


def test_get_all_operands(client, fill_db):
    response = client.get(url_for("rpn.operand.list_all_operands"))
    assert response.status_code == 200