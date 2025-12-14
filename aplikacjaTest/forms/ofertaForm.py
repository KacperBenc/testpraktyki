from django import forms
from ..models import Oferta
from aplikacjaTest.models import Uzytkownik

ROLA_CHOICES = Uzytkownik.Role.choices

class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ["pracodawca", "opis", "rodzaj_zgloszenia", "dostepnosc_oferty"]

class UzytkownikFilterForm(forms.Form):
    rola = forms.MultipleChoiceField(
        choices=ROLA_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple  # albo forms.SelectMultiple
    )
    login = forms.CharField(required=False)
    adres_mailowy = forms.CharField(required=False)
    numer_telefonu = forms.CharField(required=False)