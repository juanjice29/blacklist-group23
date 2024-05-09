import unittest
from src.commands.usuario.crear import Crear
from src.errors.errors import ResourcesRequired, ResourcesAlreadyExist
from src.models import db, Usuario


from src.main import app
import unittest
class TestCrear(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_crear_valid_user(self):
        with self.app.app_context():
            crear_command = Crear(
                username='test_user',
                password='test_password',
                email='test@example.com',
                dni='123456789',
                fullName='Test User',
                phoneNumber='1234567890'
            )
            result = crear_command.execute()

            self.assertEqual(result['username'], 'test_user')

    def test_crear_existing_user(self):

        with self.app.app_context():
            test_user = Usuario(id='test_crear_existing_user',username='existing_user', password='hashed_password', email='existing@example.com')
            db.session.add(test_user)
            db.session.commit()

            crear_command = Crear(
                username='existing_user',
                password='test_password',
                email='existing@example.com',
                dni='123456789',
                fullName='Test User',
                phoneNumber='1234567890'
            )

            with self.assertRaises(ResourcesAlreadyExist):
                crear_command.execute()

    def test_crear_invalid_input(self):
        with self.app.app_context():
            crear_command = Crear(
                username='',  # Invalid username
                password='test_password',
                email='invalid_email',  # Invalid email
                dni='123456789',
                fullName='Test User',
                phoneNumber='1234567890'
            )

            with self.assertRaises(ResourcesRequired):
                crear_command.execute()


if __name__ == '__main__':
    unittest.main()