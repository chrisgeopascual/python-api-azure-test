import pytest
from utils.schema_validator import validate_schema

USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "userName": {"type": ["string", "null"]},
        "password": {"type": ["string", "null"]}
    },
    "required": ["id", "userName", "password"]
}

@pytest.mark.smoke
def test_get_all_users_returns_200(users_client):
    response = users_client.get_all_users()
    assert response.status_code == 200

@pytest.mark.smoke
def test_get_all_users_returns_a_list(users_client):
    response = users_client.get_all_users()
    body = response.json()
    assert isinstance(body, list)
    assert len(body) > 0

@pytest.mark.smoke
def test_get_single_user_returns_matching_id(users_client):
    response = users_client.get_user_by_id(1)
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.regression
def test_create_user_returns_200(users_client):
    payload = {"id": 101, "userName": "testuser1", "password": "TestPass123"}
    response = users_client.create_user(payload)
    assert response.status_code == 200

@pytest.mark.regression
def test_create_user_echoes_submitted_data(users_client):
    payload = {"id": 102, "userName": "testuser2", "password": "AnotherPass456"}
    response = users_client.create_user(payload)
    body = response.json()
    assert body["userName"] == "testuser2"
    assert body["password"] == "AnotherPass456"

@pytest.mark.regression
def test_update_user_returns_200(users_client):
    payload = {"id": 1, "userName": "updateduser", "password": "UpdatedPass789"}
    response = users_client.update_user(1, payload)
    assert response.status_code == 200

@pytest.mark.regression
def test_delete_user_returns_200(users_client):
    response = users_client.delete_user(1)
    assert response.status_code == 200

@pytest.mark.regression
def test_get_user_invalid_id_returns_404(users_client):
    response = users_client.get_user_by_id(999999)
    assert response.status_code == 404

@pytest.mark.regression
def test_create_user_malformed_payload_returns_200_with_defaults(users_client):
    """
    Confirmed behavior: FakeRESTApi does not enforce required fields on POST.
    Missing id defaults to 0, missing password defaults to None (nullable string),
    while userName (explicitly provided) is preserved as submitted.
    """
    payload = {"userName": "MissingFields"}
    response = users_client.create_user(payload)
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 0
    assert body["userName"] == "MissingFields"
    assert body["password"] is None

@pytest.mark.regression
def test_single_user_matches_schema(users_client):
    response = users_client.get_user_by_id(1)
    validate_schema(response.json(), USER_SCHEMA)

@pytest.mark.regression
def test_all_users_list_matches_schema(users_client):
    response = users_client.get_all_users()
    for user in response.json():
        validate_schema(user, USER_SCHEMA)