
# Projekt: Download Revo Data

## Opis

Aplikacja Django, która pobiera dane z zewnętrznego API, przetwarza je i wyświetla na ekranie. Komenda `download_revo_data` umożliwia pobranie danych z API i ich dalsze przetwarzanie.

## Instrukcja użycia komendy `download_revo_data`

### 1. Użycie komendy Django

Komenda `download_revo_data` jest zdefiniowana w Twojej aplikacji Django i umożliwia pobranie danych z serwera API oraz ich przetworzenie.

#### Jak używać komendy:
1. Upewnij się, że Twoje środowisko Django jest skonfigurowane (w tym środowisko wirtualne i zależności).
2. Zmień katalog na katalog główny Twojej aplikacji Django (gdzie znajduje się `manage.py`).
3. Uruchom poniższą komendę w terminalu:

```bash
python manage.py download_revo_data
```

#### Działanie komendy:
- Komenda pobiera dane z API (adres endpointu jest ustawiany za pomocą zmiennej środowiskowej `REVO_ENDPOINT`, domyślnie jest to `revo`).
- Po pobraniu danych, dane są walidowane i przetwarzane.
- Wyniki są wyświetlane na ekranie w postaci informacji o każdym rekordzie, np.:
  ```bash
  ID: 1, Name: Test, Is Active: True, tags : ['one', 'two']
  ID: 2, Name: Another, Is Active: False, tags : []
  ```
- Jeśli API zwróci kod odpowiedzi różny od 200, pojawi się komunikat o błędzie:
  ```bash
  Response status code is not 200.
  ```
- Jeśli dane nie będą poprawne, np. w przypadku błędnego typu danych, komenda zgłosi odpowiedni wyjątek:
  ```bash
  Data validation error: ...
  ```

## Jak uruchomić testy

Testy zostały napisane za pomocą frameworka `pytest`. Aby uruchomić testy, musisz mieć zainstalowane `pytest` i `pytest-django`.

### Kroki do uruchomienia testów:

1. **Zainstaluj pytest**:
   Jeśli jeszcze tego nie zrobiłeś, zainstaluj `pytest` oraz `pytest-django` w środowisku wirtualnym:

   ```bash
   pip install pytest pytest-django
   ```

2. **Upewnij się, że masz poprawnie skonfigurowane środowisko Django**:
   Przed uruchomieniem testów upewnij się, że masz odpowiednią konfigurację Django, tj. ustawione `DATABASES`, `INSTALLED_APPS` oraz inne zmienne konfiguracyjne w pliku `settings.py`.

3. **Uruchom testy**:
   Aby uruchomić testy, wejdź do katalogu głównego aplikacji Django (gdzie znajduje się `manage.py`) i uruchom polecenie:

   ```bash
   pytest
   ```

   Testy zostaną uruchomione, a wynik będzie wyświetlany w terminalu. Jeśli testy zakończą się powodzeniem, zobaczysz coś podobnego do:

   ```bash
   ============================= test session starts ==============================
   collected 4 items

   tests/test_download_revo_data.py ....                                         [100%]

   ============================== 4 passed in 1.23 seconds ==============================
   ```

   W przeciwnym przypadku, `pytest` wyświetli informacje o niezaliczonych testach i szczegóły błędów.

4. **Uruchomienie testów z określoną opcją (np. tylko testy jednej funkcji)**:
   Jeśli chcesz uruchomić tylko jeden test, możesz to zrobić, dodając opcję `-k`, np.:

   ```bash
   pytest -k test_api_returns_non_200
   ```

   Powyższe polecenie uruchomi tylko test `test_api_returns_non_200`.

5. **Sprawdzanie logów**:
   W przypadku testów, które wykorzystują logowanie (np. test `test_api_returns_non_200`), możesz użyć opcji `-s`, aby wyświetlić logi na konsoli:

   ```bash
   pytest -s
   ```

## Podsumowanie:

- **Użycie komendy Django**: Uruchamiasz ją za pomocą `python manage.py download_revo_data`.
- **Testowanie**: Używasz `pytest` do uruchamiania testów, po wcześniejszym zainstalowaniu odpowiednich pakietów (`pytest`, `pytest-django`).
- **Logowanie w testach**: Testy z logowaniem możesz przechwycić za pomocą `caplog` i sprawdzić, czy odpowiednie komunikaty zostały zapisane.
