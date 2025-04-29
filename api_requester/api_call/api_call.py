import requests
import logging
from requests.exceptions import RequestException
from pydantic import BaseModel, ValidationError
from typing import List

logger = logging.getLogger(__name__)


class revo_data(BaseModel):
    """
    Model danych Revo, który jest używany do walidacji i przechowywania danych pobranych z API.

    Attributes:
        id (int): Unikalny identyfikator elementu.
        name (str): Nazwa elementu.
        is_active (bool): Flaga wskazująca, czy element jest aktywny.
        tags (List[str]): Lista tagów powiązanych z elementem.
    """

    id: int
    name: str
    is_active: bool
    tags: List[str]


class ApiRequester:
    """
    Klasa odpowiedzialna za komunikację z API i przetwarzanie danych.

    Metody:
        make_request(endpoint, method, headers): Wysyła zapytanie HTTP do API i przetwarza odpowiedź.
        data_processing(data): Przetwarza dane i waliduje je za pomocą Pydantic.
        download_data(endpoint): Pobiera dane z API, przetwarza je i zwraca.
    """

    def make_request(self, endpoint, method="GET", headers=None):
        """
        Wysyła zapytanie HTTP do API i przetwarza odpowiedź.

        Jeśli odpowiedź ma status różny od 200 lub wystąpi błąd, loguje odpowiedni komunikat.

        Args:
            endpoint (str): URL endpointa, do którego wysyłane jest zapytanie.
            method (str, optional): Metoda HTTP, domyślnie "GET".
            headers (dict, optional): Nagłówki HTTP, domyślnie None.

        Returns:
            dict or None: Zwraca dane w formacie JSON, jeśli odpowiedź jest poprawna, w przeciwnym razie None.
        """
        try:
            response = requests.request(method, endpoint, headers=headers, timeout=5)
            try:
                revo_data = response.json()
            except ValueError:
                logger.error("Response content is not valid JSON")
                return None
            except RequestException as e:
                logger.error("An error occurred: %s", e)
                return None
            if response.status_code != 200:
                logger.warning("Response status code is not 200.")
                return revo_data
            return revo_data
        except RequestException as e:
            logger.error("An error occurred: %s", e)
            return None

    def data_processing(self, data):
        """
        Przetwarza dane i waliduje je przy użyciu Pydantic.

        W przypadku błędu walidacji danych (np. nieprawidłowy typ) rzuca wyjątek ValueError.

        Args:
            data (list): Lista słowników z danymi do przetworzenia.

        Returns:
            list: Lista przetworzonych i zwalidowanych danych.

        Raises:
            ValueError: Jeśli dane nie przejdą walidacji Pydantic.
        """
        processed_data = data
        result = []
        for item in processed_data:
            try:
                revo_data(**item)  # Validate the data using Pydantic
                result.append(item)
            except ValidationError as e:
                raise ValueError(f"Data validation error{e}")
        logger.info("Data processed successfully")
        return result

    def download_data(self, endpoint):
        """
        Pobiera dane z API, przetwarza je i zwraca.

        Jeśli dane są poprawne, zwraca je po przetworzeniu. Jeśli wystąpił błąd podczas pobierania lub
        przetwarzania danych, zwraca None.

        Args:
            endpoint (str): URL endpointa, z którego dane mają zostać pobrane.

        Returns:
            list or None: Lista przetworzonych danych, jeśli operacja się powiodła, w przeciwnym razie None.
        """
        response = self.make_request(endpoint)
        if response:
            return self.data_processing(response)
        else:
            return None
