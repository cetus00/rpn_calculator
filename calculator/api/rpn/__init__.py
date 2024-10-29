from flask import Blueprint

from calculator.api.rpn.operand import operand_bp
from calculator.api.rpn.stack import stack_bp

rpn_bp = Blueprint("rpn", __name__, url_prefix="/rpn")

rpn_bp.register_blueprint(stack_bp)
rpn_bp.register_blueprint(operand_bp)