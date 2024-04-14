from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Blacklist(db.Model):
    id = db.Column(db.String(128), primary_key=True, nullable=False)
    app_uuid = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(48), nullable=False)
    blocked_reason = db.Column(db.String(256))
    ip_request = db.Column(db.String(32))
    createdAt = db.Column(db.DateTime)
    usuario = db.Column(db.String(128), db.ForeignKey('usuario.id'))
    __tablename__ = 'blacklist'

class Usuario(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(32), nullable=False, unique=True)
    phoneNumber = db.Column(db.String(20))
    dni = db.Column(db.String(20))
    fullName = db.Column(db.String(70))
    password = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128))
    token = db.Column(db.String(512))
    status = db.Column(db.String(20), default="POR_VERIFICAR")
    expireAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)
    updateAt = db.Column(db.DateTime)
    __tablename__ = 'usuario'


class BlacklistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Blacklist
        include_relationships = True
        load_instance = True
        
    id = fields.String()

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        include_fk = True
        load_instance = True
        
    id = fields.String()