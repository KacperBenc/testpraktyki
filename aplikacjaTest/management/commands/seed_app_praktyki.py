from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date

from aplikacjaTest.models import (
    Uzytkownik,
    Kraj,
    Miasto,
    Adres,
    Pracodawca,
    Oferta,
    OpiekunPraktyk,
    Student,
    PracownikBK,
)


class Command(BaseCommand):
    help = "Seed prostych danych do aplikacji praktyki."

    def handle(self, *args, **options):
        self.stdout.write("Tworzę dane...")

        # --- 1. Jeden adres wspólny ---
        kraj, _ = Kraj.objects.get_or_create(nazwa="Polska")
        miasto, _ = Miasto.objects.get_or_create(nazwa="Kraków")
        adres, _ = Adres.objects.get_or_create(
            kraj=kraj,
            miasto=miasto,
            ulica="ul. Uniwersytecka",
            numer_budynku="10",
            kod_pocztowy="30-100",
        )

        password = "test1234"

        # --- 2. PRZYKŁADOWI UŻYTKOWNICY ---

        studenci = [
            ("anna.kowalska", "Anna", "Kowalska"),
            ("piotr.zalewski", "Piotr", "Zalewski"),
            ("julia.rosinska", "Julia", "Rosińska"),
            ("michal.grabowski", "Michał", "Grabowski"),
            ("karolina.wisniewska", "Karolina", "Wiśniewska"),
        ]

        opiekunowie = [
            ("adam.nowak", "Adam", "Nowak"),
            ("maria.kaczmarek", "Maria", "Kaczmarek"),
            ("jan.wojcik", "Jan", "Wójcik"),
            ("ewa.lis", "Ewa", "Lis"),
            ("tomasz.baran", "Tomasz", "Baran"),
        ]

        pracownicy_bk = [
            ("alicja.rutkowska", "Alicja", "Rutkowska"),
            ("bartosz.maj", "Bartosz", "Maj"),
            ("katarzyna.krol", "Katarzyna", "Król"),
            ("lukasz.adamczyk", "Łukasz", "Adamczyk"),
            ("monika.pawlak", "Monika", "Pawlak"),
        ]

        pracodawcy = [
            ("marek.kaminski", "Marek", "Kamiński", "SoftVision Sp. z o.o."),
            ("paulina.szewczyk", "Paulina", "Szewczyk", "TechNova S.A."),
            ("krzysztof.urban", "Krzysztof", "Urban", "BlueCode Labs"),
            ("natalia.czarnecka", "Natalia", "Czarnecka", "GreenSoft"),
            ("dariusz.wilk", "Dariusz", "Wilk", "Bright Future IT"),
        ]

        # --- 3. FUNKCJA pomocnicza ---

        def create_user(login, imie, nazwisko, rola, email=None):
            if email is None:
                email = f"{login}@example.com"

            dj_user, _ = User.objects.get_or_create(
                username=login,
                defaults={"email": email},
            )
            dj_user.set_password(password)
            dj_user.save()

            uzytkownik, _ = Uzytkownik.objects.get_or_create(
                login=login,
                defaults={
                    "django_user": dj_user,
                    "rola": rola,
                    "haslo": password,
                    "status_konta": True,
                    "numer_telefonu": "500000000",
                    "adres_mailowy": email,
                },
            )
            return uzytkownik

        # --- 4. Tworzenie STUDENTÓW ---

        for idx, (login, imie, nazwisko) in enumerate(studenci, start=1):
            u = create_user(login, imie, nazwisko, Uzytkownik.Role.STUDENT)
            Student.objects.get_or_create(
                uzytkownik=u,
                defaults={
                    "adres": adres,
                    "imie": imie,
                    "nazwisko": nazwisko,
                    "data_urodzenia": date(2000, 1, min(idx, 28)),
                    "numer_indeksu": f"S2025{idx:03d}",
                },
            )

        # --- 5. Tworzenie OPIEKUNÓW ---

        for (login, imie, nazwisko) in opiekunowie:
            u = create_user(login, imie, nazwisko, Uzytkownik.Role.OPIEKUN)
            OpiekunPraktyk.objects.get_or_create(
                uzytkownik=u,
                defaults={"imie": imie, "nazwisko": nazwisko},
            )

        # --- 6. Tworzenie PRACOWNIKÓW BK ---

        for (login, imie, nazwisko) in pracownicy_bk:
            u = create_user(login, imie, nazwisko, Uzytkownik.Role.PRACOWNIK_BK)
            PracownikBK.objects.get_or_create(
                uzytkownik=u,
                defaults={"imie": imie, "nazwisko": nazwisko},
            )

        # --- 7. Tworzenie PRACODAWCÓW ---

        pracodawcy_objs = []

        for (login, imie, nazwisko, firma) in pracodawcy:
            u = create_user(login, imie, nazwisko, Uzytkownik.Role.PRACODAWCA)
            prac, _ = Pracodawca.objects.get_or_create(
                uzytkownik=u,
                defaults={
                    "adres": adres,
                    "imie_przedstawiciela": imie,
                    "nazwisko_przedstawiciela": nazwisko,
                    "nazwa_firmy": firma,
                    "nip": "1234567890",
                },
            )
            pracodawcy_objs.append(prac)

        # --- 8. Tworzenie OFERT (10 sztuk) ---

        rodzaje = list(Oferta.Rodzaj)
        dostepnosci = list(Oferta.Dostepnosc)

        for i in range(1, 11):
            pracodawca = pracodawcy_objs[(i - 1) % len(pracodawcy_objs)]
            Oferta.objects.get_or_create(
                pracodawca=pracodawca,
                opis=f"Praktyki {i} w firmie {pracodawca.nazwa_firmy}.",
                rodzaj_zgloszenia=rodzaje[i % len(rodzaje)].value,
                dostepnosc_oferty=dostepnosci[i % len(dostepnosci)].value,
            )

        self.stdout.write(self.style.SUCCESS("Seed gotowy!"))
        self.stdout.write(self.style.SUCCESS("Hasło do wszystkich kont: test1234"))
