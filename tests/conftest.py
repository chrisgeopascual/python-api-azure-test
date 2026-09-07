import pytest
from api_clients.books_client import BooksClient
from api_clients.authors_client import AuthorsClient

@pytest.fixture
def books_client():
    return BooksClient()

@pytest.fixture
def authors_client():
    return AuthorsClient()