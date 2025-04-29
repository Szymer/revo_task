import os
from django.core.management.base import BaseCommand
from api_requester.api_call.api_call import ApiRequester


class Command(BaseCommand):
    """
    Komenda Django do pobierania danych Revo z serwera i ich wyświetlania.

    Ta komenda łączy się z API, pobiera dane i przetwarza je, a następnie wyświetla szczegóły
    każdego elementu (id, nazwa, status aktywności i tagi). Obsługuje błędy związane z pobieraniem
    danych, w tym błędy walidacji danych.

    Attributes:
        help (str): Pomoc opisująca funkcjonalność komendy.
    """

    help = "Import revo data from the server"

    def handle(self, *args, **kwargs):
        """
        Główna funkcja komendy, która wykonuje proces pobierania i przetwarzania danych Revo.

        Funkcja najpierw inicjalizuje obiekt `ApiRequester`, który łączy się z API i pobiera dane.
        Następnie waliduje i przetwarza te dane. Jeśli wystąpią jakiekolwiek błędy, są one
        odpowiednio obsługiwane i komunikaty o błędach są wyświetlane w konsoli.

        Jeśli dane zostaną pomyślnie pobrane i przetworzone, funkcja wyświetli je w konsoli.

        Args:
            *args: Argumenty przekazywane do komendy.
            **kwargs: Słownik dodatkowych argumentów przekazywanych do komendy.

        Raises:
            ValueError: W przypadku nieprawidłowych danych zwróconych przez API.
        """
        endpoint = os.getenv(
            "REVO_ENDPIONT", "revo"
        )  # Replace with your actual endpoint
        # Initialize the API requester
        api_requester = ApiRequester()
        try:
            revo_data = api_requester.download_data(endpoint=endpoint)
        except ValueError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            raise
        if not revo_data:
            self.stdout.write(self.style.ERROR("Failed to download Revo data."))
            return
        self.stdout.write(self.style.SUCCESS("Revo data downloaded successfully."))

        for data in revo_data:
            id = data.get("id")
            name = data.get("name")
            is_active = data.get("is_active")
            tags = data.get("tags", [])
            print(f"ID: {id}, Name: {name}, Is Active: {is_active}, tags : {tags}")
