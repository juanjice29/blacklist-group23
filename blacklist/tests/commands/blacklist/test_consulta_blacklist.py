import unittest
from src.commands.blacklist.consulta_blacklist import ConsultaBlacklist
from src.errors.errors import ResourcesRequired, ResourcesAlreadyExist
from src.models import db, Blacklist
from src.main import app

class TestConsultaBlacklist(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_execute_with_valid_email(self):
        with self.app.app_context():
            test_blacklist = Blacklist(id='test_uuid',app_uuid='test_uuid_app', email='test@example.com', blocked_reason='Test reason', ip_request='127.0.0.1', usuario='test_user')        
            db.session.add(test_blacklist)
            db.session.commit()
            email = "test@example.com"
            consulta = ConsultaBlacklist(email)
            _ , status_code = consulta.execute()

            self.assertEqual(status_code, 200)

    def test_execute_with_invalid_email(self):
        with self.app.app_context():
            email = "test@example.com"
            consulta = ConsultaBlacklist(email)
            _ , status_code = consulta.execute()

            self.assertEqual(status_code, 404)
    

    def test_execute_with_invalid_email(self):
        invalid_email = "invalid_email"
        consulta = ConsultaBlacklist(invalid_email)

        with self.assertRaises(ResourcesRequired):
            consulta.execute()