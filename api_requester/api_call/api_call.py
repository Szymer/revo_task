import requests
import logging
from requests.exceptions import RequestException
from rest_framework.exceptions import APIException  # Importujemy APIException z DRF

logger = logging.getLogger(__name__)

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
            return dupa
        try:
            response = requests.request(method, endpoint,headers=headers, timeout=5)
            try:
                revo_data = response.json()
            except ValueError:
                logger.error("Response content is not valid JSON")
                return None
            except RequestException as e:
                logger.error("An error occurred: %s", e)
                return None
            if response.status_code != 200:
                logger.error("Request failed with status code: %s", response.status_code)
                return  "!=200"  
            return revo_data
        except RequestException as e:
            logger.error("An error occurred: %s", e)
            return None

    def data_processing(self, data):
        processed_data = data
        logger.info(f"Processing data: {processed_data}")
        
        return processed_data
    def download_data(self, endpoint):
        response = self.make_request(endpoint)
        if response:
            return self.data_processing(response)
        else:
            return None
