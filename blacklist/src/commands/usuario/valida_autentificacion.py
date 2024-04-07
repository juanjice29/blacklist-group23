from ..base_command import BaseCommannd
from ...errors.errors import  ExpiredInformation
from ...models import  Usuario, UsuarioSchema
from datetime import datetime


    
usuario_schema = UsuarioSchema()
    
class ValidaAutentificacion(BaseCommannd):
  def __init__(self, id):
    self.id = id
  
  def execute(self):
    usuario = Usuario.query.filter(Usuario.id == self.id).first()
    if usuario is not None:
        if(usuario.expireAt is not None and usuario.expireAt > datetime.utcnow()):
            return usuario_schema.dump(usuario)
    raise ExpiredInformation