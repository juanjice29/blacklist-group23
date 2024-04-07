from ..base_command import BaseCommannd
from ...validations import is_empty, es_correo_valido, obtener_fecha_actual
from ...errors.errors import ResourcesRequired, ResourcesAlreadyExist
from ...models import  db, Blacklist, BlacklistSchema
from sqlalchemy import or_
import uuid

blacklist_schema = BlacklistSchema()

class ConsultaBlacklist(BaseCommannd):
  def __init__(self, email):
    self.email = email

  def execute(self):
    if is_empty(self.email) or not es_correo_valido(self.email):
      raise ResourcesRequired
    blacklist = Blacklist.query.filter(Blacklist.email == self.email).first()
    if blacklist is None:
      return '', 404
    return '', 200