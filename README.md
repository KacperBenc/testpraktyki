# System Zarządzania Praktykami Studenckimi

## Opis projektu
System Zarządzania Praktykami Studenckimi to aplikacja webowa wspierająca proces organizacji, nadzoru i dokumentowania praktyk oraz staży realizowanych przez studentów. Celem systemu jest poprawa komunikacji między studentami, uczelnią i pracodawcami oraz zapewnienie przejrzystego i bezpiecznego zarządzania praktykami.

## Funkcjonalności
- Rejestracja i logowanie użytkowników: studentów, pracodawców, opiekunów praktyk oraz pracowników Biura Karier
- Zarządzanie ofertami praktyk i staży
- Składanie i akceptacja zgłoszeń na praktyki
- Dokumentowanie przebiegu praktyk (dziennik praktyk, raporty, załączniki)
- Generowanie dokumentów PDF (zawiadomienia, raporty)
- Komunikacja i powiadomienia wewnątrz systemu
- Wystawianie i przeglądanie ocen pracodawców
- Panel administracyjny do zarządzania użytkownikami, ofertami i innymi danymi
- Wysoka dostępność i bezpieczeństwo danych zgodnie z wymogami RODO

## Technologie
- **Backend:** Django (Python) z architekturą MVT
- **Frontend:** Django Templates (HTML, CSS, JavaScript, Bootstrap)
- **Baza danych:** dev: SQLite, prod: PostgreSQL
- **Konteneryzacja:** Docker (opcjonalnie)
- **System zarządzania rolami i uprawnieniami użytkowników**


## Architektura systemu
System korzysta z separacji warstw prezentacji, logiki biznesowej i warstwy danych. Dane użytkowników, ofert, zgłoszeń i dokumentacji są przechowywane w relacyjnej bazie PostgreSQL. Django ORM ułatwia integrację i zarządzanie danymi. Panel administracyjny pozwala na łatwe zarządzanie systemem.

## Instalacja i uruchomienie
1. Sklonuj repozytorium
2. Skonfiguruj bazę danych PostgreSQL (testowo SQLite)
3. (Opcjonalnie) Uruchom system w kontenerach Docker
4. Uruchom serwer Django
5. Uzyskaj dostęp do aplikacji przez przeglądarkę pod adresem http://localhost:8000

## Instrukcje użytkowania
- Studenci mogą przeglądać oferty, aplikować na praktyki i dokumentować przebieg praktyk
- Pracodawcy mogą dodawać i zarządzać ofertami po zatwierdzeniu
- Opiekunowie nadzorują przebieg praktyk i zatwierdzają zgłoszenia
- Pracownicy Biura Karier zarządzają użytkownikami, ofertami i monitorują system


# Info teraz dla nas :)
- dodany jest testowy plik, który dodaje do bazy jakieś testowe dane
- polecam usunąć plik db.sqlite3 (chyba że chcecie zostawić swoje dane, które wpisywaliście)
- zrobić migracje - plik db.sqlite3 utworzy się od nowa
- załadować testowe dane
```bash
rm db.sqlite3
python manage.py migrate
python manage.py init_role
python manage.py seed_app_praktyki  # wywołanie dodania kilku testowych użytkowników i ofert
```

przykładowi użytkownicy:
- **student**: piotr.zalewski
- **opiekun**: ewa.lis
- **pracownik bk**: katarzyna.krol
- **pracodawca**: krzysztof.urban
- **hasło**: test1234

Pełna lista użytkowników w kodzie init_role.py

# Role i uprawnienia
W systemie są zdefiniowane role biznesowe oraz powiązane z nimi uprawnienia, które kontrolują dostęp do widoków Django i operacji na danych
## Role użytkowników (Uzytkownik.Role)
- Student – może przeglądać oferty, zgłaszać się na praktyki, przeglądać i edytować swój profil, przeglądać własne zgłoszenia, wypełniać dziennik praktyk i wystawiać oceny pracodawcy.
- Pracodawca – może przeglądać oferty, tworzyć nowe oferty praktyk/staży, zarządzać swoimi ofertami, przeglądać zgłoszenia studentów na swoje oferty (w zakresie zdefiniowanym w widokach) oraz edytować swój profil.
- Opiekun Praktyk – może przeglądać i nadzorować zgłoszenia przypisanych studentów, mieć wgląd w przebieg praktyk (zgłoszenia, ewentualne zaliczenia), a także edytować własny profil.
- Pracownik BK – rola administracyjno‑koordynacyjna, może przeglądać listy użytkowników, zarządzać statusem kont (aktywacja/dezaktywacja), przeglądać i edytować zgłoszenia studentów oraz mieć rozszerzony podgląd profili.

## Niestandardowe uprawnienia (TestPraktyki.Meta.permissions)
Uprawnienia są zdefiniowane jako meta‑permissions w modelu TestPraktyki i mogą być przypisywane do grup lub indywidualnych kont w panelu admina.
- add_offer_portal – „Może dodawać ofertę w portalu”
    - Umożliwia dostęp do widoku dodawania oferty (OfertaCreateView, ścieżka /oferty/nowa/).
- view_own_applications – „Może widzieć własne zgłoszenia”
  - Steruje dostępem do listy własnych zgłoszeń studenta (widok moje_zgloszenia, ścieżka /zgloszenia/moje/).
- view_assigned_applications – „Może widzieć przypisane zgłoszenia”
  - Pozwala opiekunowi przeglądać zgłoszenia przypisane do niego (przypisane_zgloszenia, /zgloszenia/przypisane/).
- view_students – „Może widzieć listę studentów”
  - Używane w widoku listy użytkowników (UzytkownikListView, /uzytkownicy/), zwykle przypisane pracownikowi BK; daje wgląd w listę studentów (i innych użytkowników) z filtrami.
- view_tutors – „Może widzieć listę opiekunów”
  - Uprawnienie do przeglądania listy opiekunów praktyk (logika może być realizowana we wspólnym widoku listy użytkowników lub dedykowanych widokach).
- view_employers – „Może widzieć listę pracodawców”
  - Uprawnienie do przeglądania listy pracodawców, np. w celu weryfikacji i administracji ich kontami.
- view_users – „Może widzieć listę użytkowników”
  - Ogólniejsze uprawnienie do wglądu w pełną listę użytkowników, wykorzystywane w panelu BK lub administracji.
- view_user_profile – „Może widzieć profil użytkownika”
  - Kontroluje dostęp do widoku szczegółów profilu (UzytkownikDetailView, /profil/), zwłaszcza przy podglądzie profili innych osób niż aktualnie zalogowany użytkownik.
- change_user_profile – „Może edytować profil użytkownika”
  - Umożliwia edycję profilu (UzytkownikUpdateView, /profil/<pk>/edycja), w tym danych użytkownika i powiązanych modeli roli/adresu.
- change_user_status – „Może zmieniać status konta użytkownika”
  - Daje dostęp do akcji aktywacji/dezaktywacji kont przez widok UzytkownikToggleAktywnoscView (/profil/<pk>/toggle), typowo przypisane pracownikowi BK lub administratorowi.

# Konfiguracja środowiska (.env)
W projekcie Django 5 środowisko konfigurowane jest przez zmienne z pliku .env, ładowane za pomocą biblioteki
1. Utwórz plik .env w katalogu głównym projektu (tam, gdzie znajduje się manage.py i settings.py).
2. Uzupełnij go podstawowymi zmiennymi konfiguracyjnymi, na przykład:
```
# Tryb developerski (True/False)
DEBUG=True

# Klucz bezpieczeństwa Django
SECRET_KEY=zmien_to_na_losowy_klucz

# Konfiguracja bazy danych
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# (opcjonalnie) konfiguracja PostgreSQL zamiast SQLite
DB_ENGINE=django.db.backends.postgresql
DB_NAME=praktyki
DB_USER=postgres
DB_PASSWORD=haslo
DB_HOST=localhost
DB_PORT=5432
```

3. Upewnij się, że plik .env jest dodany do .gitignore, aby nie trafił do repozytorium (szczególnie SECRET_KEY i dane do bazy).
4. Przy uruchamianiu projektu Django (python manage.py runserver) ustawienia zostaną odczytane z .env poprzez environ.Env.read_env(...) w settings.py, co pozwala łatwo zmieniać konfigurację między środowiskiem developerskim a produkcyjnym.