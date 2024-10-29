from flask import Blueprint, request
from sqlalchemy import insert, func, update

from calculator.db import db
from calculator.models import Stacks


stack_bp = Blueprint("stack", __name__, url_prefix="/stack")

STACK_NOT_FOUND = "Stack not found"

@stack_bp.route("/", methods=['GET'])
def get_all_stacks():
    stacks = db.session.query(Stacks).all()
    stacks_list = [{"id": stack.id, "stack": stack.stack} for stack in stacks]
    return stacks_list, 200

@stack_bp.route("/", methods=['POST'])
def create_new_stack():
    stmt = insert(Stacks).returning(Stacks.id)
    result = db.session.execute(stmt)

    new_id = result.scalar()
    db.session.commit()
    return {"id": new_id}, 200

@stack_bp.route("/<int:stack_id>", methods=['GET'])
def get_stack(stack_id):
    stack = db.session.query(Stacks.stack).filter(Stacks.id == stack_id).first()
    if stack is None:
        return "", 404
    return {"stack": stack[0]}, 200

@stack_bp.route("/<int:stack_id>", methods=['POST'])
def add_value_to_stack(stack_id):
    data = request.get_json()
    value_to_append = data.get("value")

    if value_to_append is None:
        return "Value is required", 400
    if type(value_to_append) not in (int, float):
        return "Value should be an integer or a float", 400
    stack = db.session.query(Stacks.stack).filter(Stacks.id == stack_id).first()
    if stack is None:
        return STACK_NOT_FOUND, 404

    stmt = (
        update(Stacks)
        .where(Stacks.id == stack_id)
        .values(stack=func.array_append(Stacks.stack, value_to_append))
    )

    db.session.execute(stmt)
    db.session.commit()

    return "", 204

@stack_bp.route("/<int:stack_id>", methods=['DELETE'])
def delete_stack(stack_id):
    stack_entry = db.session.query(Stacks).filter(Stacks.id == stack_id).first()

    if stack_entry is None:
        return STACK_NOT_FOUND, 404

    db.session.delete(stack_entry)
    db.session.commit()
    return "", 204