from ..base_command import BaseCommannd
from ...validations import is_empty, es_correo_valido, obtener_fecha_actual
from ...errors.errors import ResourcesRequired, ResourcesAlreadyExist
from ...models import  db, Blacklist, BlacklistSchema
from sqlalchemy import or_
import uuid

blacklist_schema = BlacklistSchema()

class AltaBlacklist(BaseCommannd):
  def __init__(self, email, app_uuid, blocked_reason, usuario, ip_peticion):
    self.email = email
    self.app_uuid = app_uuid
    self.blocked_reason = blocked_reason
    self.usuario = usuario
    self.ip_peticion = ip_peticion

  def execute(self):
    if is_empty(self.app_uuid) or is_empty(self.email) or not es_correo_valido(self.email):
      raise ResourcesRequired
    blacklist = Blacklist.query.filter(or_(Blacklist.app_uuid == self.app_uuid, Blacklist.email == self.email)).first()
    if blacklist is None:
      time = obtener_fecha_actual()
      nuevo_blacklist = Blacklist(id=str(uuid.uuid4()),app_uuid=self.app_uuid.strip(), email=self.email.strip(), blocked_reason=self.blocked_reason, ip_request=self.ip_peticion, createdAt=time, usuario=self.usuario)
      db.session.add(nuevo_blacklist)
      db.session.commit()
      return blacklist_schema.dump(nuevo_blacklist)
    else:
      raise ResourcesAlreadyExist