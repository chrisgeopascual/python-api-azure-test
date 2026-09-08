import pytest
from utils.schema_validator import validate_schema

COVERPHOTO_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "idBook": {"type": "integer"},
        "url": {"type": ["string", "null"]}
    },
    "required": ["id", "idBook", "url"]
}

@pytest.mark.smoke
def test_get_all_coverphotos_returns_200(coverphotos_client):
    response = coverphotos_client.get_all_coverphotos()
    assert response.status_code == 200

@pytest.mark.smoke
def test_get_all_coverphotos_returns_a_list(coverphotos_client):
    response = coverphotos_client.get_all_coverphotos()
    body = response.json()
    assert isinstance(body, list)
    assert len(body) > 0

@pytest.mark.smoke
def test_get_single_coverphoto_returns_matching_id(coverphotos_client):
    response = coverphotos_client.get_coverphoto_by_id(1)
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.smoke
def test_get_coverphoto_by_book_id_returns_200(coverphotos_client):
    """
    Cross-resource lookup, same pattern as Authors' get_authors_by_book_id.
    """
    response = coverphotos_client.get_coverphoto_by_book_id(1)
    assert response.status_code == 200

@pytest.mark.regression
def test_create_coverphoto_returns_200(coverphotos_client):
    payload = {"id": 101, "idBook": 1, "url": "https://example.com/cover.jpg"}
    response = coverphotos_client.create_coverphoto(payload)
    assert response.status_code == 200

@pytest.mark.regression
def test_create_coverphoto_echoes_submitted_data(coverphotos_client):
    payload = {"id": 102, "idBook": 2, "url": "https://example.com/another-cover.jpg"}
    response = coverphotos_client.create_coverphoto(payload)
    body = response.json()
    assert body["idBook"] == 2
    assert body["url"] == "https://example.com/another-cover.jpg"

@pytest.mark.regression
def test_update_coverphoto_returns_200(coverphotos_client):
    payload = {"id": 1, "idBook": 1, "url": "https://example.com/updated-cover.jpg"}
    response = coverphotos_client.update_coverphoto(1, payload)
    assert response.status_code == 200

@pytest.mark.regression
def test_delete_coverphoto_returns_200(coverphotos_client):
    response = coverphotos_client.delete_coverphoto(1)
    assert response.status_code == 200

@pytest.mark.regression
def test_get_coverphoto_invalid_id_returns_404(coverphotos_client):
    response = coverphotos_client.get_coverphoto_by_id(999999)
    assert response.status_code == 404

@pytest.mark.regression
def test_create_coverphoto_malformed_payload_returns_200_with_defaults(coverphotos_client):
    """
    Confirmed behavior: FakeRESTApi does not enforce required fields on POST.
    Missing id defaults to 0, missing url defaults to None (nullable string),
    while idBook (explicitly provided) is preserved as submitted.
    """
    payload = {"idBook": 1}
    response = coverphotos_client.create_coverphoto(payload)
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 0
    assert body["idBook"] == 1
    assert body["url"] is None

@pytest.mark.regression
def test_single_coverphoto_matches_schema(coverphotos_client):
    response = coverphotos_client.get_coverphoto_by_id(1)
    validate_schema(response.json(), COVERPHOTO_SCHEMA)

@pytest.mark.regression
def test_all_coverphotos_list_matches_schema(coverphotos_client):
    response = coverphotos_client.get_all_coverphotos()
    for coverphoto in response.json():
        validate_schema(coverphoto, COVERPHOTO_SCHEMA)