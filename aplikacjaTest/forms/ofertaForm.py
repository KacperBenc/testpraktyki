from django import forms
from ..models import Oferta
from aplikacjaTest.models import Uzytkownik

ROLA_CHOICES = Uzytkownik.Role.choices


class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ["pracodawca", "opis", "rodzaj_zgloszenia", "dostepnosc_oferty"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Sprawdź rolę użytkownika
        is_pracownik_bk = False
        is_student = False

        if user:
            uzytkownik = getattr(user, "uzytkownik", None)
            if uzytkownik:
                is_pracownik_bk = uzytkownik.rola == Uzytkownik.Role.PRACOWNIK_BK
                is_student = uzytkownik.rola == Uzytkownik.Role.STUDENT

        # Logika dla PRACOWNIKÓW BK - widzą wszystkie pola
        if is_pracownik_bk:
            pass  # Wszystkie pola dostępne

        # Logika dla STUDENTÓW
        elif is_student:
            # Student może wybrać pracodawcę (lub zaproponować nowego)
            # Pole pracodawcy pozostaje widoczne

            # Student może wybrać rodzaj zgłoszenia (Praca/Praktyki/Staż)
            # Pole rodzaj_zgloszenia pozostaje widoczne

            # Dostępność automatycznie ustawiona na "Niepubliczna" i ukryta
            if "dostepnosc_oferty" in self.fields:
                self.fields["dostepnosc_oferty"].initial = (
                    Oferta.Dostepnosc.NIEPUBLICZNA
                )
                self.fields["dostepnosc_oferty"].widget = forms.HiddenInput()
                self.fields["dostepnosc_oferty"].required = False

        # Logika dla PRACODAWCÓW
        else:
            # Ukryj pole pracodawcy
            if "pracodawca" in self.fields:
                self.fields["pracodawca"].widget = forms.HiddenInput()
                self.fields["pracodawca"].required = False

            # Ustaw rodzaj zgłoszenia na "Praktyki" i ukryj pole
            if "rodzaj_zgloszenia" in self.fields:
                self.fields["rodzaj_zgloszenia"].initial = Oferta.Rodzaj.PRAKTYKI
                self.fields["rodzaj_zgloszenia"].widget = forms.HiddenInput()


class UzytkownikFilterForm(forms.Form):
    rola = forms.MultipleChoiceField(
        choices=ROLA_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,  # albo forms.SelectMultiple
    )
    login = forms.CharField(required=False)
    adres_mailowy = forms.CharField(required=False)
    numer_telefonu = forms.CharField(required=False)
