import pytest
from flask.testing import FlaskClient
from chatbot_parser import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_command(client):
    data = {
        "command": "test_command",
        "server_url": "http://localhost:5050"
    }
    response = client.post('/register', json=data)
    assert response.status_code == 200
    assert response.json["status"] == "success"
