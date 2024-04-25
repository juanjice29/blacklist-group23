import pytest
from unittest.mock import patch, MagicMock
from errors.errors import ResourcesAlreadyExist
from models import Blacklist
from commands.blacklist.alta_blacklist import AltaBlacklist
from commands.blacklist.consulta_blacklist import ConsultaBlacklist


@pytest.fixture
def new_blacklist_data():
    return {
        "email": "test@example.com",
        "app_uuid": "uuid-test-123",
        "blocked_reason": "testing reasons",
        "usuario": "test_user",
        "ip_peticion": "192.168.1.1",
    }


@pytest.fixture
def existing_blacklist_entry():
    return Blacklist(
        email="test@example.com",
        app_uuid="uuid-test-123",
        blocked_reason="testing reasons",
        usuario="test_user",
        ip_request="192.168.1.1",
        id="1",
        createdAt="2021-01-01T00:00:00",
    )


def test_alta_blacklist_execute_new_entry(client, new_blacklist_data):
    with client.application.app_context():
        # Assuming db.session.add and db.session.commit are mocked if needed
        alta = AltaBlacklist(**new_blacklist_data)
        result = alta.execute()
        assert result["email"] == new_blacklist_data["email"]


def test_alta_blacklist_execute_existing_entry(client, existing_blacklist_entry):
    with client.application.app_context():
        # Prepare the db to simulate an existing entry
        with patch("models.db.session.query") as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = (
                existing_blacklist_entry
            )
            model_dict = {
                "email": existing_blacklist_entry.email,
                "app_uuid": existing_blacklist_entry.app_uuid,
                "blocked_reason": existing_blacklist_entry.blocked_reason,
                "usuario": existing_blacklist_entry.usuario,
                "ip_peticion": existing_blacklist_entry.ip_request,  # Ensure the attribute name matches the model/expected name
            }
            alta = AltaBlacklist(**model_dict)
            with pytest.raises(
                ResourcesAlreadyExist
            ):  # Expecting a specific exception for duplicate
                alta.execute()


def test_consulta_blacklist_execute_found(client, existing_blacklist_entry):
    with client.application.app_context():
        with patch("models.db.session.query") as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = (
                existing_blacklist_entry
            )
            consulta = ConsultaBlacklist(email="test@example.com")
            result = consulta.execute()
            assert result[1] == 200


def test_consulta_blacklist_execute_not_found(client):
    with client.application.app_context():
        with patch("models.db.session.query") as mock_query:
            mock_query.return_value.filter.return_value.first.return_value = None
            consulta = ConsultaBlacklist(email="test2@example.com")
            result = consulta.execute()
            assert result == ("", 404)
