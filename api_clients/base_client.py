import requests
from config.config import BASE_URL

class BaseClient:

    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    def get(self, endpoint, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

    def post(self, endpoint, json=None, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", json=json, **kwargs)

    def put(self, endpoint, json=None, **kwargs):
        return self.session.put(f"{self.base_url}{endpoint}", json=json, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.session.delete(f"{self.base_url}{endpoint}", **kwargs)