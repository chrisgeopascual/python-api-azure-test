from api_clients.base_client import BaseClient

class BooksClient(BaseClient):
    RESOURCE = "/api/v1/Books"

    def get_all_books(self):
        return self.get(self.RESOURCE)

    def get_book_by_id(self, book_id):
        return self.get(f"{self.RESOURCE}/{book_id}")

    def create_book(self, payload):
        return self.post(self.RESOURCE, json=payload)

    def update_book(self, book_id, payload):
        return self.put(f"{self.RESOURCE}/{book_id}", json=payload)

    def delete_book(self, book_id):
        return self.delete(f"{self.RESOURCE}/{book_id}")