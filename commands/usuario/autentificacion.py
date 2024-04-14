from ..base_command import BaseCommannd
from errors.errors import ResourcesRequired, NotFound
from flask_jwt_extended import  create_access_token
from models import  db, Usuario, UsuarioSchema
from validations import is_empty, obtener_password
from datetime import datetime, timedelta
import hashlib
import secrets

    
usuario_schema = UsuarioSchema()
    
class Autentificar(BaseCommannd):
  def __init__(self, username, password):
    self.username = username
    self.password = password
  
  def execute(self):
    if is_empty(self.username) or is_empty(self.password):
        raise ResourcesRequired
    usuario = Usuario.query.filter(Usuario.username == self.username).first()
    if usuario is not None:
        if(usuario.password != hashlib.sha256(obtener_password(self.password, usuario.email).encode()).hexdigest()):
            raise NotFound
        salt = secrets.token_hex(8)
        token = create_access_token(identity=usuario.id)
        usuario.salt = salt
        usuario.token = token
        usuario.expireAt = (datetime.utcnow() + timedelta(hours=3)).isoformat()
        usuario.updateAt = datetime.utcnow().isoformat()
        db.session.commit()
        return usuario_schema.dump(usuario)
    else:
        raise NotFound