import unittest
from src.commands.usuario.actualiza import Actualiza
from src.errors.errors import ResourcesRequired
from src.models import db, Usuario
from src.main import app

class TestActualiza(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_actualiza_valid_input(self):
        with self.app.app_context():
            test_user = Usuario(
                id=1,
                status='POR_VERIFICAR',
                dni='123456789',
                fullName='Test User',
                phoneNumber='1234567890',
                username='picovoltagewe',
                email='jamirosa@grecor.com',
                password='cartagos'
            )
            db.session.add(test_user)
            db.session.commit()

            actualiza_command = Actualiza(
                id=1,
                status='NO_VERIFICADO',
                dni='987654321',
                fullName='Updated User',
                phoneNumber='9876543210'
            )
            actualiza_command.execute()

            updated_user = Usuario.query.get(1)

            self.assertEqual(updated_user.status, 'NO_VERIFICADO')
            self.assertEqual(updated_user.dni, '987654321')
            self.assertEqual(updated_user.fullName, 'Updated User')
            self.assertEqual(updated_user.phoneNumber, '9876543210')

    def test_actualiza_empty_input(self):
        with self.app.app_context():
            test_user = Usuario(
                id=1,
                status='POR_VERIFICAR',
                dni='123456789',
                fullName='Test User',
                phoneNumber='1234567890',
                username='picovoltage',
                email='jamiro@grecor.com',
                password='cartagos'
            )
            db.session.add(test_user)
            db.session.commit()

            actualiza_command = Actualiza(
                id=1,
                status='',
                dni='',
                fullName='',
                phoneNumber=''
            )

            with self.assertRaises(ResourcesRequired):
                actualiza_command.execute()