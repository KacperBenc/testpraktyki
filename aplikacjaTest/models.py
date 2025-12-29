from django.db import models
from django.contrib.auth.models import User


class TestPraktyki(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ("add_offer_portal", "Może dodawać ofertę w portalu"),
            ("change_offer_portal", "Może edytować ofertę w portalu"),
            ("delete_offer_portal", "Może usuwać ofertę z portalu"),
            ("view_own_applications", "Może widzieć własne zgłoszenia"),
            ("view_assigned_applications", "Może widzieć przypisane zgłoszenia"),
            ("view_students", "Może widzieć listę studentów"),
            ("view_tutors", "Może widzieć listę opiekunów"),
            ("view_employers", "Może widzieć listę pracodawców"),
            ("view_users", "Może widzieć listę użytkowników"),
            ("view_user_profile", "Może widzieć profil użytkownika"),
            ("change_user_profile", "Może edytować profil użytkownika"),
            ("change_user_status", "Może zmieniać status konta użytkownika"),
        ]


class Uzytkownik(models.Model):
    class Role(models.TextChoices):
        STUDENT = "Student", "Student"
        OPIEKUN = "Opiekun Praktyk", "Opiekun Praktyk"
        PRACOWNIK_BK = "Pracownik BK", "Pracownik BK"
        PRACODAWCA = "Pracodawca", "Pracodawca"

    django_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    rola = models.CharField(max_length=50, choices=Role.choices)
    login = models.CharField(max_length=50, unique=True)
    haslo = models.CharField(max_length=255)
    status_konta = models.BooleanField(null=True)
    numer_telefonu = models.CharField(max_length=15, null=True)
    adres_mailowy = models.EmailField(unique=True)

    def __str__(self):
        return self.login


class Kraj(models.Model):
    nazwa = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nazwa


class Miasto(models.Model):
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return self.nazwa


class Adres(models.Model):
    kraj = models.ForeignKey(Kraj, on_delete=models.PROTECT)
    miasto = models.ForeignKey(Miasto, on_delete=models.PROTECT)
    ulica = models.CharField(max_length=100, null=True)
    numer_budynku = models.CharField(max_length=10)
    numer_lokalu = models.CharField(max_length=10, null=True, blank=True)
    kod_pocztowy = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.ulica} {self.numer_budynku}, {self.miasto}"


class Pracodawca(models.Model):
    uzytkownik = models.OneToOneField(Uzytkownik, on_delete=models.CASCADE)
    adres = models.ForeignKey(Adres, on_delete=models.PROTECT)
    imie_przedstawiciela = models.CharField(max_length=50, null=True)
    nazwisko_przedstawiciela = models.CharField(max_length=50, null=True)
    nazwa_firmy = models.CharField(max_length=100, null=True)
    nip = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.nazwa_firmy or "(Pracodawca)"


class Student(models.Model):
    uzytkownik = models.OneToOneField(Uzytkownik, on_delete=models.CASCADE)
    adres = models.ForeignKey(Adres, on_delete=models.PROTECT)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    data_urodzenia = models.DateField()
    numer_indeksu = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.imie} {self.nazwisko} ({self.numer_indeksu})"


class OpiekunPraktyk(models.Model):
    uzytkownik = models.OneToOneField(Uzytkownik, on_delete=models.CASCADE)
    adres = models.ForeignKey(Adres, on_delete=models.PROTECT)
    imie = models.CharField(max_length=50, null=True)
    nazwisko = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


class PracownikBK(models.Model):
    uzytkownik = models.OneToOneField(Uzytkownik, on_delete=models.CASCADE)
    adres = models.ForeignKey(Adres, on_delete=models.PROTECT)
    imie = models.CharField(max_length=50, null=True)
    nazwisko = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"


class Oferta(models.Model):
    class Rodzaj(models.TextChoices):
        PRACA = "Praca zawodowa", "Praca zawodowa"
        PRAKTYKI = "Praktyki", "Praktyki"
        STAZ = "Staż", "Staż"
        JDG = "JDG", "JDG"

    class Dostepnosc(models.TextChoices):
        PUBLICZNA = "Publiczna", "Publiczna"
        NIEPUBLICZNA = "Niepubliczna", "Niepubliczna"

    pracodawca = models.ForeignKey(Pracodawca, on_delete=models.CASCADE)
    opis = models.TextField(null=True)
    rodzaj_zgloszenia = models.CharField(max_length=30, choices=Rodzaj.choices)
    dostepnosc_oferty = models.CharField(max_length=20, choices=Dostepnosc.choices)

    def __str__(self):
        return f"Oferta #{self.id} - {self.pracodawca}"


class Zgloszenie(models.Model):
    class Status(models.TextChoices):
        ZGLOSZONE = "Zgłoszone", "Zgłoszone"
        ZAAKCEPTOWANE = "Zaakceptowane", "Zaakceptowane"
        ODRZUCONE = "Odrzucone", "Odrzucone"
        ZALICZONE = "Zaliczone", "Zaliczone"
        NIEZALICZONE = "Niezaliczone", "Niezaliczone"

    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    opiekun_praktyk = models.ForeignKey(
        OpiekunPraktyk, on_delete=models.SET_NULL, null=True, blank=True
    )
    data_zgloszenia = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=Status.choices, null=True)
    ocena_dla_pracodawcy = models.IntegerField(null=True)

    def __str__(self):
        return f"Zgłoszenie #{self.id}"


class Zaliczenie(models.Model):
    zgloszenie = models.ForeignKey(Zgloszenie, on_delete=models.CASCADE)
    data_rozpoczecia = models.DateTimeField(null=True)
    data_zakonczenia = models.DateTimeField(null=True)

    def __str__(self):
        return f"Zaliczenie #{self.id}"


class Wpis(models.Model):
    zaliczenie = models.ForeignKey(Zaliczenie, on_delete=models.CASCADE)
    data_wpisu = models.DateTimeField(null=True)
    dzien_praktyk = models.DateTimeField(null=True)
    szczegoly = models.TextField(null=True)

    def __str__(self):
        return f"Wpis #{self.id}"


class Zalacznik(models.Model):
    zgloszenie = models.ForeignKey(Zgloszenie, on_delete=models.CASCADE)
    sciezka = models.CharField(max_length=500, null=True)
    data_dodania = models.DateTimeField(null=True)

    def __str__(self):
        return f"Załącznik #{self.id}"


class OcenaDlaPracodawcy(models.Model):
    zgloszenie = models.ForeignKey(Zgloszenie, on_delete=models.CASCADE)
    ocena = models.IntegerField(null=True)
    komentarz = models.TextField(null=True)

    def __str__(self):
        return f"Ocena #{self.id}"
