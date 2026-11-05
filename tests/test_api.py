import pytest
from my_app import create_app
from my_app.config import TestingConfig


@pytest.fixture
def client():
    app = create_app(TestingConfig)
    with app.test_client() as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "UP"
    assert payload["database_connected"] is True


def test_get_members(client):
    response = client.get("/api/v1/members")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert isinstance(payload["data"], list)


def test_create_member_validation_error(client):
    invalid_payload = {
        "name": "Al",
        "phone": "12345",
        "age": 12,
        "gender": "Male",
        "plan": "Basic Plan",
        "batch": "Morning (06:00 AM - 08:00 AM)",
    }
    response = client.post("/api/v1/members", json=invalid_payload)
    assert response.status_code == 422
    payload = response.get_json()
    assert payload["success"] is False
    assert payload["error"]["code"] == "VALIDATION_ERROR"


def test_create_and_delete_member_flow(client):
    valid_payload = {
        "name": "Vikram Rathore",
        "phone": "9998887776",
        "age": 27,
        "gender": "Male",
        "plan": "VIP Pro Plan",
        "batch": "Evening (05:00 PM - 07:00 PM)",
        "email": "vikram.rathore@example.com",
        "status": "Paid",
    }
    create_response = client.post("/api/v1/members", json=valid_payload)
    assert create_response.status_code == 201
    created_data = create_response.get_json()["data"]
    member_id = created_data["id"]

    assert created_data["name"] == "Vikram Rathore"
    assert created_data["trainer"] == "Senior Coach Vikram"

    # Test Duplicate phone number constraint
    duplicate_response = client.post("/api/v1/members", json=valid_payload)
    assert duplicate_response.status_code == 409

    # Test fee status toggle
    patch_response = client.patch(
        f"/api/v1/members/{member_id}/fee-status",
        json={"status": "Pending"},
    )
    assert patch_response.status_code == 200
    assert patch_response.get_json()["data"]["status"] == "Pending"

    # Test Delete
    delete_response = client.delete(f"/api/v1/members/{member_id}")
    assert delete_response.status_code == 200

    # Test 404 after delete
    get_after_delete = client.get(f"/api/v1/members/{member_id}")
    assert get_after_delete.status_code == 404


def test_bmi_calculation(client):
    bmi_payload = {
        "height_cm": 180.0,
        "weight_kg": 75.0,
        "age": 25,
    }
    response = client.post("/api/v1/fitness/bmi", json=bmi_payload)
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    data = payload["data"]
    assert data["bmi_score"] == 23.1
    assert data["category"] == "Normal"
    assert "Hypertrophy" not in data["workout_advice"] or "balanced" in data["workout_advice"].lower()


def test_stats_endpoint(client):
    response = client.get("/api/v1/stats")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert "total_members" in payload["data"]
    assert "financials" in payload["data"]
