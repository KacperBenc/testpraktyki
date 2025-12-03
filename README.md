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
- **Frontend:** Django Templates (HTML, CSS, JavaScript)
- **Baza danych:** PostgreSQL
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
python manage.py seed_app_praktyki  # wywołanie dodania kilku testowych użytkowników i ofert
```