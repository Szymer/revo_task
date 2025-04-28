import os
import requests

from requests.exceptions import RequestException


class ApiRequester:
    def __init__(self):
        self.base_url = os.getenv('API_BASE_URL', 'https://api.example.com')  # Replace with your API base URL

    def make_request(self, endpoint, method='GET', params=None, data=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.request(method, url, params=params, data=data, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def data_processing(self, data):
        processed_data = data

    def download_data(self, endpoint):
        response = self.make_request(endpoint)
        if response:
            self.data_processing(response)
        else:
            print("Failed to download data.")
            return None
