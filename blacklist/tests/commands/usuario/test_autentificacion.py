import unittest
from src.commands.usuario.autentificacion import Autentificar
from src.models import db, Usuario
from src.main import app
from src.errors.errors import NotFound, ResourcesRequired

class TestAutentificacion(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_autentificar_valid_credentials(self):
        with self.app.app_context():
            test_user = Usuario(id='test_autentificar_valid_credentials',username='test_user', password='hashed_password', email='test@example.com')
            db.session.add(test_user)
            db.session.commit()

            autentificar_command = Autentificar(username='test_user', password='hashed_password')
            with self.assertRaises(NotFound):
                result = autentificar_command.execute()

                self.assertEqual(result['username'], 'test_user')
                self.assertIsNotNone(result['token'])

    def test_autentificar_invalid_credentials(self):
        with self.app.app_context():
            test_user = Usuario(id='test_autentificar_invalid_credentials',username='test_user', password='hashed_password', email='test@example.com')
            db.session.add(test_user)
            db.session.commit()

            autentificar_command = Autentificar(username='test_user', password='wrong_password')

            with self.assertRaises(NotFound):
                autentificar_command.execute()

    def test_autentificar_without_parameters(self):
        with self.app.app_context():
            test_user = Usuario(id='test_autentificar_without_parameters',username='test_user', password='hashed_password', email='test@example.com')
            db.session.add(test_user)
            db.session.commit()

            autentificar_command = Autentificar(username='test_user', password='')

            with self.assertRaises(ResourcesRequired):
                autentificar_command.execute()
