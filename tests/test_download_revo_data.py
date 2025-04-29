import pytest
from unittest import mock
from django.core.management import call_command
from api_requester.api_call.api_call import ApiRequester


# Mock poprawnych danych
valid_data = [
    {"id": 1, "name": "Test", "is_active": True, "tags": ["one", "two"]},
    {"id": 2, "name": "Another", "is_active": False, "tags": []},
]

# Mock danych o nieprawidłowym typie (id jako string)
invalid_data = [{"id": "wrong", "name": "Test", "is_active": True, "tags": []}]


class MockResponse:
    """
    Klasa pomocnicza do symulowania odpowiedzi HTTP w testach.
    """

    def __init__(self, json_data, status_code):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json


@pytest.mark.django_db
def test_api_connection_error(monkeypatch):
    """
    Testuje, czy wystąpi wyjątek w przypadku problemu z połączeniem.
    """

    def mock_make_request(self, endpoint, method="GET", headers=None):
        raise Exception("Connection error")

    monkeypatch.setattr(ApiRequester, "make_request", mock_make_request)

    with pytest.raises(Exception, match="Connection error"):
        call_command("download_revo_data")


@pytest.mark.django_db
def test_api_returns_non_200(monkeypatch, caplog):
    """
    Testuje, czy logowanie błędu działa poprawnie, gdy API zwraca status inny niż 200.
    """

    def mock_request(self, endpoint, method="GET", headers=None, timeout=5):
        return MockResponse(valid_data, 404)

    monkeypatch.setattr("requests.request", mock_request)

    with caplog.at_level("WARNING"):  # Możemy ustawić poziom logowania
        call_command("download_revo_data")

    assert "Response status code is not 200." in caplog.text


@pytest.mark.django_db
def test_api_returns_invalid_data(monkeypatch):
    """
    Testuje, czy występuje wyjątek ValueError, gdy API zwraca dane z błędnym typem (np. string zamiast int).
    """

    def mock_make_request(self, endpoint, method="GET", headers=None):
        return invalid_data

    monkeypatch.setattr(ApiRequester, "make_request", mock_make_request)

    with pytest.raises(ValueError, match="Data validation error"):
        call_command("download_revo_data")


@pytest.mark.django_db
def test_api_returns_valid_data(monkeypatch):
    """
    Testuje, czy dane są poprawnie przetwarzane i wyświetlane, gdy API zwraca poprawne dane.
    """

    def mock_make_request(self, endpoint, method="GET", headers=None):
        return valid_data

    monkeypatch.setattr(ApiRequester, "make_request", mock_make_request)

    with mock.patch("builtins.print") as mock_print:
        call_command("download_revo_data")
        mock_print.assert_any_call(
            "ID: 1, Name: Test, Is Active: True, tags : ['one', 'two']"
        )
        mock_print.assert_any_call("ID: 2, Name: Another, Is Active: False, tags : []")
