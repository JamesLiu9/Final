import pytest
from flask.testing import FlaskClient
from shrug_command_server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_shrug_command(client):
    data = {
        "command": "shrug",
        "message": "Test message"
    }
    response = client.post('/execute', json={"data": data})
    assert response.status_code == 200
    assert "data" in response.json
    assert response.json["data"]["message"].endswith("¯\_(ツ)_/¯")
