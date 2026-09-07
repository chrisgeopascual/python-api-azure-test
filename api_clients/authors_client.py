from api_clients.base_client import BaseClient

class AuthorsClient(BaseClient):
    RESOURCE = "/api/v1/Authors"

    def get_all_authors(self):
        return self.get(self.RESOURCE)

    def get_author_by_id(self, author_id):
        return self.get(f"{self.RESOURCE}/{author_id}")

    def get_authors_by_book_id(self, book_id):
        return self.get(f"{self.RESOURCE}/authors/books/{book_id}")

    def create_author(self, payload):
        return self.post(self.RESOURCE, json=payload)

    def update_author(self, author_id, payload):
        return self.put(f"{self.RESOURCE}/{author_id}", json=payload)

    def delete_author(self, author_id):
        return self.delete(f"{self.RESOURCE}/{author_id}")