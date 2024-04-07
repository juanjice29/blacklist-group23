from flask import jsonify, request, Blueprint
from ..commands.reset import Reset
from flask_jwt_extended import jwt_required

general_blueprint = Blueprint('general', __name__)

@general_blueprint.route('/ping', methods = ['GET'])
def ping():
    return "pong", 200

@general_blueprint.route('/reset', methods = ['POST'])
@jwt_required()
def reset():
    Reset().execute()
    return jsonify({"msg": "Todos los datos fueron eliminados"}), 200