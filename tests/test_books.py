import pytest
from test_data.payloads import build_book_payload
from utils.schema_validator import validate_schema

BOOK_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": ["string", "null"]},
        "description": {"type": ["string", "null"]},
        "pageCount": {"type": "integer"},
        "excerpt": {"type": ["string", "null"]},
        "publishDate": {"type": "string"}
    },
    "required": ["id", "title", "description", "pageCount", "excerpt", "publishDate"]
}

@pytest.mark.smoke
def test_get_all_books_returns_200(books_client):
    response = books_client.get_all_books()
    assert response.status_code == 200

@pytest.mark.smoke
def test_get_all_books_returns_a_list(books_client):
    response = books_client.get_all_books()
    body = response.json()
    assert isinstance(body, list)
    assert len(body) > 0

@pytest.mark.smoke
def test_get_single_book_returns_matching_id(books_client):
    response = books_client.get_book_by_id(1)
    assert response.status_code == 200
    assert response.json()["id"] == 1

@pytest.mark.regression
def test_post_book_returns_returns_200(books_client):
    payload = build_book_payload()
    response = books_client.create_book(payload)
    assert response.status_code == 200

@pytest.mark.regression
def test_post_book_echoes_submitted_title(books_client):
    payload = build_book_payload()
    response = books_client.create_book(payload)
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["pageCount"] == payload["pageCount"]

@pytest.mark.regression
def test_update_book_returns_200(books_client):
    payload = build_book_payload(book_id=1)
    response = books_client.update_book(1, payload)
    assert response.status_code == 200

@pytest.mark.regression
def test_delete_book_returns_200(books_client):
    response = books_client.delete_book(1)
    assert response.status_code == 200

@pytest.mark.regression
def test_get_book_invalid_id_returns_404(books_client):
    response = books_client.get_book_by_id(999999)
    assert response.status_code == 404

@pytest.mark.regression
def test_single_book_matches_schema(books_client):
    response = books_client.get_book_by_id(1)
    validate_schema(response.json(), BOOK_SCHEMA)

@pytest.mark.regression
def test_all_books_list_matches_schema(books_client):
    response = books_client.get_all_books()
    for book in response.json():
        validate_schema(book, BOOK_SCHEMA)

@pytest.mark.regression
def test_create_book_malformed_payload_returns_200_with_defaults(books_client):
    """
    Confirmed behavior: FakeRESTApi does not enforce required fields on POST.
    Missing fields default to their .NET type defaults rather than being rejected:
    int -> 0, nullable string -> None, DateTime -> '0001-01-01T00:00:00'.
    """
    payload = {"title": "MissingFields"}
    response = books_client.create_book(payload)
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "MissingFields"
    assert body["id"] == 0
    assert body["description"] is None
    assert body["pageCount"] == 0
    assert body["excerpt"] is None
    assert body["publishDate"] == "0001-01-01T00:00:00"