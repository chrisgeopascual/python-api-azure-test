import pytest
from api_clients.books_client import BooksClient
from api_clients.authors_client import AuthorsClient
from api_clients.activities_client import ActivitiesClient
from api_clients.coverphotos_client import CoverPhotosClient
from api_clients.users_client import UsersClient


@pytest.fixture
def books_client():
    return BooksClient()

@pytest.fixture
def authors_client():
    return AuthorsClient()

@pytest.fixture
def activities_client():
    return ActivitiesClient()

@pytest.fixture
def coverphotos_client():
    return CoverPhotosClient()

@pytest.fixture
def users_client():
    return UsersClient()