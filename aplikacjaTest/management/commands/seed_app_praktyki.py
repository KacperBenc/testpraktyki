from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
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

            # mapowanie ról z modelu Uzytkownik na nazwy grup
            role_to_group = {
                Uzytkownik.Role.STUDENT: "student",
                Uzytkownik.Role.OPIEKUN: "opiekun",
                Uzytkownik.Role.PRACOWNIK_BK: "pracownikBK",
                Uzytkownik.Role.PRACODAWCA: "pracodawca",
            }
            group_name = role_to_group.get(rola)
            if group_name:
                try:
                    group = Group.objects.get(name=group_name)
                    dj_user.groups.add(group)
                except Group.DoesNotExist:
                    print(f"Brak grupy {group_name}.")

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
                defaults={"imie": imie, "nazwisko": nazwisko, "adres": adres},
            )

        # --- 6. Tworzenie PRACOWNIKÓW BK ---

        for (login, imie, nazwisko) in pracownicy_bk:
            u = create_user(login, imie, nazwisko, Uzytkownik.Role.PRACOWNIK_BK)
            PracownikBK.objects.get_or_create(
                uzytkownik=u,
                defaults={"imie": imie, "nazwisko": nazwisko, "adres": adres},
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

        opisy = [
            "Junior Developer: Poszukujemy Junior Developera, który z entuzjazmem podchodzi do kopiowania rozwiązań ze Stack Overflow i wierzy, że komentarze w kodzie naprawdę coś znaczą. Na tym stanowisku będziesz walczyć z konfiguracją środowiska i zależnościami, które „przecież działały u kolegi”. Szukamy osoby, która nie boi się momentu, gdy senior powie: „odpal to u siebie lokalnie” i traktuje to jako szansę na rozwój.",

            "Senior Developer: Do naszego zespołu szukamy Senior Developera, który widział już prawie wszystko, łącznie z własnym kodem sprzed lat i potrafi wyciągać z tego wnioski. Oczekujemy znajomości wielu sposobów rozwiązywania problemów oraz umiejętności wyboru tego, który naprawdę ma sens, nawet jeśli jest najmniej przyjemny. Jeśli Twoje ulubione zdanie brzmi „to kiedyś trzeba będzie przepisać”, idealnie odnajdziesz się w naszym kodbase.",

            "DevOps Engineer: Szukamy DevOps Engineera, który czuje się jak ryba w wodzie w świecie serwerów, kontenerów i plików YAML. Na tym stanowisku będziesz tym, kto nie wierzy w „u mnie działa”, tylko patrzy w logi jak w gwiazdy i wyciąga z nich wnioski. Oczekujemy, że pomożesz nam zbudować i utrzymać rozbudowane dashboardy oraz zadbasz o niski poziom frustracji zespołu (własny możesz mierzyć wedle uznania).",

            "Frontend Developer: Do naszego zespołu szukamy Frontend Developera z wyczuciem estetyki i obsesją na punkcie pikseli. Twoim zadaniem będzie tworzenie i dopieszczanie interfejsów, które działają równie dobrze, jak wyglądają, nawet w starciu z upartymi przeglądarkami. Jeśli potrafisz spędzić trzy godziny nad odcieniem przycisku i nadal uważać, że to był dobrze wykorzystany czas, pasujesz idealnie.",

            "Backend Developer: Poszukujemy Backend Developera, dla którego dobrze zaprojektowane API jest ważniejsze niż to, jak wygląda sam przycisk „Wyślij”. Na tym stanowisku będziesz pracować z endpointami, bazami danych i logami, które czytasz jak poranną gazetę. Szukamy osoby, która rozumie, że użytkownik Cię nie widzi, ale bez Twojej pracy wszystko rozpadnie się w kilka sekund.",

            "Tester / QA Engineer: Szukamy Testera / QA Engineera, który z zamiłowaniem udowadnia, że nic nie działa tak dobrze, jak się wszystkim wydaje. Będziesz odpowiedzialny za wyszukiwanie błędów w najdziwniejszych zakamarkach aplikacji, także tam, gdzie nawet autor kodu nie pamięta, że coś istnieje. Idealny kandydat to osoba, która nie boi się słyszeć „tego przypadku użycia nikt nie sprawdzi w realnym życiu” i lubi udowadniać, że jest inaczej.",

            "Product Owner: Do naszego zespołu poszukujemy Product Ownera, który potrafi tłumaczyć biznesowe wizje na język zrozumiały dla developerów. Twoim naturalnym środowiskiem będzie backlog pełen pomysłów, zadań i priorytetów, które trzeba sensownie poukładać. Jeśli potrafisz przyjść z jednym prostym pomysłem i wyjść z piętnastoma dobrze opisanymi user story, to właśnie Ciebie szukamy.",

            "Scrum Master: Szukamy Scrum Mastera, który zadba o to, aby nasze 15-minutowe stand-upy naprawdę trwały 15 minut, a nie przeradzały się w maraton narzekań. Na tym stanowisku będziesz usprawniać procesy, wspierać zespół w usuwaniu blokad i pilnować, by tablica z zadaniami żyła, a nie tylko ładnie wyglądała. Idealny kandydat to osoba, która nie boi się zadawać pytania: „co blokuje Twój ticket?”.",

            "UX/UI Designer: Poszukujemy UX/UI Designera, który rozumie potrzeby użytkowników lepiej niż oni sami i potrafi zamienić je w czytelne, estetyczne interfejsy. Będziesz projektować makiety, prototypy oraz współpracować z developerami przy ich wdrażaniu, pilnując, by rzeczywistość przeglądarek jak najmniej psuła Twoją wizję. Jeśli potrafisz godzinami dyskutować o marginesach i potwierdzać swoje decyzje badaniami, świetnie odnajdziesz się w naszym zespole.",

            "Administrator Systemów: Do naszej organizacji szukamy Administratora Systemów, który z pełnym spokojem zarządza serwerami, usługami i infrastrukturą sieciową. Na tym stanowisku będziesz dbać o dostępność systemów, bezpieczeństwo oraz szybkie reagowanie na incydenty, także te pojawiające się o nieprzyzwoitych porach. Jeśli wciąż wierzysz, że dobrze wykonany restart potrafi zdziałać cuda, ale równie chętnie sięgasz po bardziej wyrafinowane narzędzia, zapraszamy do aplikowania."
        ]

        for i in range(1, 11):
            pracodawca = pracodawcy_objs[(i - 1) % len(pracodawcy_objs)]
            Oferta.objects.get_or_create(
                pracodawca=pracodawca,
                opis=opisy[i-1],
                rodzaj_zgloszenia=rodzaje[i % len(rodzaje)].value,
                dostepnosc_oferty=dostepnosci[i % len(dostepnosci)].value,
            )

        self.stdout.write(self.style.SUCCESS("Seed gotowy!"))
        self.stdout.write(self.style.SUCCESS("Hasło do wszystkich kont: test1234"))
