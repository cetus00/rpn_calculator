import operator

from flask import Blueprint

from calculator.api.rpn.stack import STACK_NOT_FOUND
from calculator.db import db
from calculator.models import Stacks

operand_bp = Blueprint("operand", __name__, url_prefix="/op")

operands = {
        "add": operator.add,
        "sub": operator.sub,
        "mul": operator.mul,
        "div": operator.truediv
    }

@operand_bp.route("/", methods=['GET'])
def list_all_operands():
    return list(operands.keys()), 200

@operand_bp.route("/<string:operand>/stack/<int:stack_id>", methods=['POST'])
def apply_operand_to_stack(operand, stack_id):

    if operand not in operands.keys():
        return "Operand is not supported", 404
    stack = db.session.query(Stacks.stack).filter(Stacks.id == stack_id).first()
    if stack is None:
        return STACK_NOT_FOUND, 404
    if len(stack[0]) < 2:
        return f"Not enough values to apply an operand on a stack {stack[0]}", 422

    a,b = stack[0][-2:]
    try:
        new_value = operands[operand](a,b)
    except ZeroDivisionError:
        return "Zero division", 422

    db.session.query(Stacks).filter(Stacks.id == stack_id).update({"stack": stack[0][:-2] + [new_value]})

    db.session.commit()
    return "", 204