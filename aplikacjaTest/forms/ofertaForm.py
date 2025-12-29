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

        # Sprawdź czy użytkownik jest Pracownikiem BK
        is_pracownik_bk = False
        if user:
            uzytkownik = getattr(user, "uzytkownik", None)
            if uzytkownik:
                is_pracownik_bk = uzytkownik.rola == Uzytkownik.Role.PRACOWNIK_BK

        # Dla pracodawców: ukryj pole pracodawcy
        if not is_pracownik_bk and "pracodawca" in self.fields:
            self.fields["pracodawca"].widget = forms.HiddenInput()
            self.fields["pracodawca"].required = False

        # Dla pracodawców: ustaw rodzaj zgłoszenia na "Praktyki" i ukryj pole
        if not is_pracownik_bk and "rodzaj_zgloszenia" in self.fields:
            self.fields["rodzaj_zgloszenia"].initial = "Praktyki"
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
