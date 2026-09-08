from api_clients.base_client import BaseClient

class ActivitiesClient(BaseClient):
    RESOURCE = "/api/v1/Activities"

    def get_all_activities(self):
        return self.get(self.RESOURCE)

    def get_activity_by_id(self, activity_id):
        return self.get(f"{self.RESOURCE}/{activity_id}")

    def create_activity(self, payload):
        return self.post(self.RESOURCE, json=payload)

    def update_activity(self, activity_id, payload):
        return self.put(f"{self.RESOURCE}/{activity_id}", json=payload)

    def delete_activity(self, activity_id):
        return self.delete(f"{self.RESOURCE}/{activity_id}")