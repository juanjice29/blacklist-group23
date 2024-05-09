import unittest
from src.commands.blacklist.alta_blacklist import AltaBlacklist
from src.errors.errors import ResourcesAlreadyExist
from src.models import db, Blacklist
from src.main import app

class TestAltaBlacklist(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


    def test_crear_blacklist(self):
        with self.app.app_context():
            crear_command = AltaBlacklist(
                email='test@example.com',
                app_uuid='test_uuid',
                blocked_reason='Test reason',
                usuario='test_user',
                ip_peticion='127.0.0.1'
            )
            result = crear_command.execute()

            self.assertEqual(result['app_uuid'], 'test_uuid')

    def test_crear_existing_blacklist(self):
        with self.app.app_context():
            test_blacklist = Blacklist(id='test_uuid',app_uuid='test_uuid_app', email='test@example.com', blocked_reason='Test reason', ip_request='127.0.0.1', usuario='test_user')        
            db.session.add(test_blacklist)
            db.session.commit()

            crear_command = AltaBlacklist(
                email='test@example.com',
                app_uuid='test_uuid',
                blocked_reason='Test reason',
                usuario='test_user',
                ip_peticion='127.0.0.1'
            )

            with self.assertRaises(ResourcesAlreadyExist):
                crear_command.execute()


if __name__ == '__main__':
    unittest.main()
