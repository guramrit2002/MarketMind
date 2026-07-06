from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_response_has_request_id_header() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert "x-request-id" in response.headers
    assert response.headers["x-request-id"] != ""


def test_each_request_gets_unique_request_id() -> None:
    first = client.get("/health").headers["x-request-id"]
    second = client.get("/health").headers["x-request-id"]

    assert first != second
