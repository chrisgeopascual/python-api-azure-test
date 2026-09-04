import pytest
from test_data.payloads import build_book_payload

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

@pytest.mark.smoke
def test_post_book_returns_returns_200(books_client):
    payload = build_book_payload()
    response = books_client.create_book(payload)
    assert response.status_code == 200

@pytest.mark.smoke
def test_post_book_echoes_submitted_title(books_client):
    payload = build_book_payload()
    response = books_client.create_book(payload)
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["pageCount"] == payload["pageCount"]