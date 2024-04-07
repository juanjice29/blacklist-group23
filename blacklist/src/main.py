import os 
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from .blueprints.usuarios import usuarios_blueprint
from .blueprints.general import general_blueprint
from .blueprints.blacklist import blacklist_blueprint
from .errors.errors import ApiError
from flask_sqlalchemy import SQLAlchemy
from .models import db
import logging
from datetime import timedelta


dotenv_path =  '../.env.template'
loaded = load_dotenv(dotenv_path)

app = Flask(__name__)
app.register_blueprint(usuarios_blueprint)
app.register_blueprint(general_blueprint)
app.register_blueprint(blacklist_blueprint)

database_uri="postgresql+psycopg2://{}:{}@{}:{}/{}".format(os.environ.get("DB_USER"),os.environ.get("DB_PASSWORD"),os.environ.get("DB_HOST"),os.environ.get("DB_PORT"),os.environ.get("DB_NAME")) if not os.environ.get("ENV") == 'test' else "sqlite:///test.db"
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
app.config['PROPAGATE_EXCEPTIONS'] = True

cors = CORS(app)

api = Api(app)

jwt = JWTManager(app)

app.logger.setLevel(logging.INFO)
handler = logging.FileHandler('app.log')
app.logger.addHandler(handler)
app.logger.info('Inicializando aplicacion')

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description,
      "version": os.environ.get("VERSION")
    }
    return jsonify(response), err.code