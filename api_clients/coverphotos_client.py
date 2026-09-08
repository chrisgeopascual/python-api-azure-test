from api_clients.base_client import BaseClient

class CoverPhotosClient(BaseClient):
    RESOURCE = "/api/v1/CoverPhotos"

    def get_all_coverphotos(self):
        return self.get(self.RESOURCE)

    def get_coverphoto_by_id(self, coverphoto_id):
        return self.get(f"{self.RESOURCE}/{coverphoto_id}")

    def get_coverphoto_by_book_id(self, book_id):
        return self.get(f"{self.RESOURCE}/books/covers/{book_id}")

    def create_coverphoto(self, payload):
        return self.post(self.RESOURCE, json=payload)

    def update_coverphoto(self, coverphoto_id, payload):
        return self.put(f"{self.RESOURCE}/{coverphoto_id}", json=payload)

    def delete_coverphoto(self, coverphoto_id):
        return self.delete(f"{self.RESOURCE}/{coverphoto_id}")