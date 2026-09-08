import pytest
from utils.schema_validator import validate_schema

ACTIVITY_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": ["string", "null"]},
        "dueDate": {"type": "string"},
        "completed": {"type": "boolean"}
    },
    "required": ["id", "title", "dueDate", "completed"]
}

@pytest.mark.smoke
def test_get_all_activities_returns_200(activities_client):
    response = activities_client.get_all_activities()
    assert response.status_code == 200

@pytest.mark.smoke
def test_get_all_activities_returns_a_list(activities_client):
    response = activities_client.get_all_activities()
    body = response.json()
    assert isinstance(body, list)
    assert len(body) > 0

@pytest.mark.smoke
def test_get_single_activity_returns_matching_id(activities_client):
    response = activities_client.get_activity_by_id(1)
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.regression
def test_create_activity_returns_200(activities_client):
    payload = {"id": 101, "title": "New Activity", "dueDate": "2026-12-01T00:00:00", "completed": False}
    response = activities_client.create_activity(payload)
    assert response.status_code == 200

@pytest.mark.regression
def test_create_activity_echoes_submitted_data(activities_client):
    payload = {"id": 102, "title": "Sample Activity", "dueDate": "2026-12-01T00:00:00", "completed": True}
    response = activities_client.create_activity(payload)
    body = response.json()
    assert body["title"] == "Sample Activity"
    assert body["completed"] is True

@pytest.mark.regression
def test_update_activity_returns_200(activities_client):
    payload = {"id": 1, "title": "Updated Activity", "dueDate": "2026-12-01T00:00:00", "completed": True}
    response = activities_client.update_activity(1, payload)
    assert response.status_code == 200

@pytest.mark.regression
def test_delete_activity_returns_200(activities_client):
    response = activities_client.delete_activity(1)
    assert response.status_code == 200

@pytest.mark.regression
def test_get_activity_invalid_id_returns_404(activities_client):
    response = activities_client.get_activity_by_id(999999)
    assert response.status_code == 404

@pytest.mark.regression
def test_create_activity_malformed_payload_returns_200_with_defaults(activities_client):
    """
    Confirmed behavior: FakeRESTApi does not enforce required fields on POST.
    Missing fields are defaulted to their .NET type defaults rather than rejected:
    int -> 0, DateTime -> '0001-01-01T00:00:00' (DateTime.MinValue), bool -> False.
    """
    payload = {"title": "MissingFields"}
    response = activities_client.create_activity(payload)
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "MissingFields"
    assert body["id"] == 0
    assert body["dueDate"] == "0001-01-01T00:00:00"
    assert body["completed"] is False

@pytest.mark.regression
def test_single_activity_matches_schema(activities_client):
    response = activities_client.get_activity_by_id(1)
    validate_schema(response.json(), ACTIVITY_SCHEMA)

@pytest.mark.regression
def test_all_activities_list_matches_schema(activities_client):
    response = activities_client.get_all_activities()
    for activity in response.json():
        validate_schema(activity, ACTIVITY_SCHEMA)