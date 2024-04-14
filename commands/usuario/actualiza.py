from ..base_command import BaseCommannd
from errors.errors import ResourcesRequired
from models import  db, Usuario, UsuarioSchema
from validations import is_empty, obtener_fecha_actual


usuario_schema = UsuarioSchema()

estado = ['POR_VERIFICAR', 'NO_VERIFICADO', 'VERIFICADO']

class Actualiza(BaseCommannd):
  def __init__(self, id, status, dni, fullName, phoneNumber):
    self.id = id
    self.status = status
    self.dni = dni
    self.fullName = fullName
    self.phoneNumber = phoneNumber

  def execute(self):
    contador = 0
    usuario = Usuario.query.get_or_404(self.id)
    if(not is_empty(self.status) and self.status in estado):
      contador = contador + 1
      usuario.status = self.status
    if(not is_empty(self.dni)):
      contador = contador + 1
      usuario.dni = self.dni
    if(not is_empty(self.fullName)):
      contador = contador + 1
      usuario.fullName = self.fullName
    if(not is_empty(self.phoneNumber)):
      contador = contador + 1
      usuario.phoneNumber = self.phoneNumber
    if(contador == 0):
        raise ResourcesRequired
    
    usuario.updateAt = obtener_fecha_actual()
    db.session.add(usuario)
    db.session.commit()
    return usuario_schema.dump(usuario)