from django import forms
from aplikacjaTest.models import Pracodawca


class PracodawcaForm(forms.ModelForm):
    class Meta:
        model = Pracodawca
        fields = [
            "nazwa_firmy",
            "nip",
            "imie_przedstawiciela",
            "nazwisko_przedstawiciela",
        ]
