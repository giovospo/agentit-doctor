from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200


def test_diagnosis():

    response = client.get("/diagnosis")

    assert response.status_code == 200