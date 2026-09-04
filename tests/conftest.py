import pytest
from api_clients.books_client import BooksClient

@pytest.fixture
def books_client():
    return BooksClient()