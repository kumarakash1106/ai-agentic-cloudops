
from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_investigation_returns_report():
    response = client.post(
        "/incidents/investigate",
        json={
            "title": "Checkout API latency increased",
            "description": (
                "Checkout requests became slow "
                "after deployment checkout-v42."
            ),
            "service": "checkout"
        }
    )

    assert response.status_code == 200

    result = response.json()

    assert result["status"] == "investigation_complete"
    assert result["log_count"] == 3
    assert result["metric_count"] == 1
    assert len(result["evidence"]) == 4
    assert isinstance(result["final_report"], str)
    assert len(result["final_report"]) > 0
    assert "Initial Assessment" in result["final_report"]


def test_invalid_incident_is_rejected():
    response = client.post(
        "/incidents/investigate",
        json={
            "title": "Hi",
            "description": "Too short",
            "service": "checkout"
        }
    )

    assert response.status_code == 422
