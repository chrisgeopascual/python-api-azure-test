from api_clients.base_client import BaseClient

class UsersClient(BaseClient):
    RESOURCE = "/api/v1/Users"

    def get_all_users(self):
        return self.get(self.RESOURCE)

    def get_user_by_id(self, user_id):
        return self.get(f"{self.RESOURCE}/{user_id}")

    def create_user(self, payload):
        return self.post(self.RESOURCE, json=payload)

    def update_user(self, user_id, payload):
        return self.put(f"{self.RESOURCE}/{user_id}", json=payload)

    def delete_user(self, user_id):
        return self.delete(f"{self.RESOURCE}/{user_id}")