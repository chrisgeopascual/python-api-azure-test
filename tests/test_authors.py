import pytest
from utils.schema_validator import validate_schema


AUTHOR_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "idBook": {"type": "integer"},
        "firstName": {"type": ["string", "null"]},
        "lastName": {"type": ["string", "null"]}
    },
    "required": ["id", "idBook", "firstName", "lastName"]
}

@pytest.mark.regression
def test_single_author_matches_schema(authors_client):
    response = authors_client.get_author_by_id(1)
    validate_schema(response.json(), AUTHOR_SCHEMA)

@pytest.mark.regression
def test_all_authors_list_matches_schema(authors_client):
    """
    Each item in the list response should independently match
    the same Author schema as a single-item response.
    """
    response = authors_client.get_all_authors()
    body = response.json()
    for author in body:
        validate_schema(author, AUTHOR_SCHEMA)

@pytest.mark.smoke
def test_get_all_authors_returns_200(authors_client):
    response = authors_client.get_all_authors()
    assert response.status_code == 200

@pytest.mark.smoke
def test_get_all_authors_returns_a_list(authors_client):
    response = authors_client.get_all_authors()
    body = response.json()
    assert isinstance(body, list)
    assert len(body) > 0

@pytest.mark.smoke
def test_get_single_author_returns_matching_id(authors_client):
    response = authors_client.get_author_by_id(1)
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.smoke
def test_get_authors_by_book_id_returns_200(authors_client):
    response = authors_client.get_authors_by_book_id(1)
    assert response.status_code == 200

@pytest.mark.regression
def test_create_author_returns_200(authors_client):
    payload = {
        "id": 101,
        "idBook": 1,
        "firstName": "Jane",
        "lastName": "Doe"
    }
    response = authors_client.create_author(payload)
    assert response.status_code == 200

@pytest.mark.regression
def test_create_author_echoes_submitted_data(authors_client):
    payload = {
        "id": 102,
        "idBook": 1,
        "firstName": "John",
        "lastName": "Smith"
    }
    response = authors_client.create_author(payload)
    body = response.json()
    assert body["firstName"] == "John"
    assert body["lastName"] == "Smith"

@pytest.mark.regression
def test_update_author_returns_200(authors_client):
    payload = {
        "id": 1,
        "idBook": 1,
        "firstName": "Updated",
        "lastName": "Author"
    }
    response = authors_client.update_author(1, payload)
    assert response.status_code == 200

@pytest.mark.regression
def test_delete_author_returns_200(authors_client):
    response = authors_client.delete_author(1)
    assert response.status_code == 200

@pytest.mark.regression
def test_get_author_invalid_id_returns_404(authors_client):
    response = authors_client.get_author_by_id(999999)
    assert response.status_code == 404

@pytest.mark.regression
def test_create_author_malformed_payload_returns_200_with_defaults(authors_client):
    payload = {"firstName": "MissingRequiredFields"}
    response = authors_client.create_author(payload)
    assert response.status_code == 200
    body = response.json()
    assert body["firstName"] == "MissingRequiredFields"
    assert body["id"] == 0
    assert body["lastName"] is None