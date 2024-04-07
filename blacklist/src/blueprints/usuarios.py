from flask import jsonify, request, Blueprint, current_app
from ..commands.usuario.crear import Crear
from ..commands.usuario.autentificacion import Autentificar
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
from ..commands.usuario.valida_autentificacion import ValidaAutentificacion
from ..commands.usuario.actualiza import Actualiza
from ..errors.errors import IncompleteRequest

usuarios_blueprint = Blueprint('usuarios', __name__)

@usuarios_blueprint.route('/users', methods = ['POST'])
def crear():
    json = request.get_json()
    result = Crear(json.get("username"), json.get("password"), json.get("email"), json.get("dni"), json.get("fullName"), json.get("phoneNumber")).execute()
    return jsonify({"id": result.get("id"), "createdAt": result.get("createdAt")}), 201

@usuarios_blueprint.route('/users/auth', methods = ['POST'])
def autentifica():
    json = request.get_json()
    result = Autentificar(json.get("username"), json.get("password")).execute()
    return jsonify({"id": result.get("id"),"token": result.get("token"), "expireAt": result.get("expireAt")}), 200

@usuarios_blueprint.route('/users/me', methods = ['GET'])
@jwt_required()
def valida_autentificacion():
    id = get_jwt_identity()
    current_app.logger.info(id)
    result = ValidaAutentificacion(id).execute()
    return jsonify({"id": result.get("id"),"username": result.get("username"), "email": result.get("email"), "fullName": result.get("fullName"), "dni": result.get("dni"), "phoneNumber": result.get("phoneNumber"), "status": result.get("status")}), 200

@usuarios_blueprint.route('/users/<string:id>', methods = ['PATCH'])
@jwt_required()
def update(id):
    uid = get_jwt_identity()
    json = request.get_json()
    Actualiza(uid, json.get("status"), json.get("dni"), json.get("fullName"), json.get("phoneNumber")).execute()
    return jsonify({"msg": "el usuario ha sido actualizado"}), 200

@usuarios_blueprint.route('/users/refresh', methods = ['GET'])
@jwt_required()
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({"token":access_token})