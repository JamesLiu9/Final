import pytest
from flask.testing import FlaskClient
from email_command_server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_send_email(client):
    data = {
        "email": "test@example.com",
        "subject": "Test Subject",
        "body": "Test Body"
    }
    response = client.post('/send_email', json=data)
    assert response.status_code == 200
    assert response.json["status"] == "success"
