import os 
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from blueprints.usuarios import usuarios_blueprint
from blueprints.general import general_blueprint
from blueprints.blacklist import blacklist_blueprint
from errors.errors import ApiError
from flask_sqlalchemy import SQLAlchemy
from models import db
import logging
from datetime import timedelta

application = Flask(__name__)
application.register_blueprint(usuarios_blueprint)
application.register_blueprint(general_blueprint)
application.register_blueprint(blacklist_blueprint)

database_uri="postgresql+psycopg2://{}:{}@{}:{}/{}".format("postgres","C29-j12m2024","miso23-database.ct0mggaqc8yr.us-east-1.rds.amazonaws.com","5432","blacklist")
application.config['SQLALCHEMY_DATABASE_URI'] = database_uri
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['JWT_SECRET_KEY'] = 'frase-secreta'
application.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
application.config['PROPAGATE_EXCEPTIONS'] = True

cors = CORS(application)

api = Api(application)

jwt = JWTManager(application)

application.logger.setLevel(logging.INFO)
handler = logging.FileHandler('app.log')
application.logger.addHandler(handler)
application.logger.info('Inicializando aplicacion')

app_context = application.app_context()
app_context.push()

db.init_app(application)
db.create_all()

@application.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description,
      "version": os.environ.get("VERSION")
    }
    return jsonify(response), err.code

if __name__ == "__main__":
    application.run(port = 5000, debug = True)