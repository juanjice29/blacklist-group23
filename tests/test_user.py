import pytest
from unittest.mock import patch, MagicMock
from models import Usuario,UsuarioSchema
from errors.errors import NotFound
from faker import Faker
from commands.usuario.crear import Crear
from commands.usuario.autentificacion import Autentificar

#datos mokeados
@pytest.fixture
def fake_new_user():
    fake = Faker()
    return {
        "username": fake.user_name(),
        "password": fake.password(),
        "email": fake.email(),
        "dni": str(fake.random_number(digits=8)),
        "fullName": fake.name(),
        "phoneNumber": fake.phone_number(),
        
        # Puedes agregar más campos según tus necesidades de prueba
}
#tear down para limpiar la base de datos

def test_crear_user(client, fake_new_user):
    with client.application.app_context():
        # Assuming db.session.add and db.session.commit are mocked if needed
        command = Crear(**fake_new_user)
        result = command.execute()
        print("el usuario",fake_new_user) 
        assert result["username"] == fake_new_user["username"]
        assert result["dni"] == fake_new_user["dni"]
        assert result["fullName"] == fake_new_user["fullName"]
        assert result["phoneNumber"] == fake_new_user["phoneNumber"]
        # Puedes agregar más asserts según tus necesidades de prueba


def test_autentificar(client, fake_new_user):
    # Crear un nuevo usuario para utilizarlo en la prueba de autenticación
    with client.application.app_context():
        crear_command = Crear(**fake_new_user)
        crear_command.execute()

    # Autenticar el usuario creado
    with client.application.app_context():
        autentificar_command = Autentificar(username=fake_new_user["username"], password=fake_new_user["password"])
        result = autentificar_command.execute()

        # Verificar que se autenticó correctamente
        assert result["username"] == fake_new_user["username"]
        assert result["token"]  # Verificar que se generó un token de acceso
        assert result["expireAt"]  # Verificar que se estableció una fecha de vencimiento para el token
