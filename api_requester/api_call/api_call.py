import os
import requests
import json

from requests.exceptions import RequestException


dupa = [
{
"id": 1,
"name": "Test Name 1",
"is_active": True,
"tags": ["revo", "test"]
},
{
"id": 2,
"name": "Test Name 2",
"is_active": False,
"tags": []
}
]


class ApiRequester:

    def make_request(self, endpoint, method='GET', headers=None):
        if endpoint == "revo":
            # Simulate a response for the "revo" endpoint
            return json.dumps(dupa, indent=2)
        try:
            response = requests.request(method, endpoint,headers=headers)
     
            return response.json()
        except RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def data_processing(self, data):
        processed_data = data
        print(f"Processing data: {processed_data}")
        return processed_data
    def download_data(self, endpoint):
        response = self.make_request(endpoint)
        if response:
            self.data_processing(response)
        else:
            return None
