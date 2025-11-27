from django import forms
from aplikacjaTest.models import Adres, Kraj


class AdresForm(forms.ModelForm):
    # zamiast FK do Miasto — pole tekstowe
    miasto_nazwa = forms.CharField(label="Miasto")

    class Meta:
        model = Adres
        fields = [
            "kraj",
            "miasto_nazwa",
            "ulica",
            "numer_budynku",
            "numer_lokalu",
            "kod_pocztowy",
        ]

    def clean_numer_lokalu(self):
        value = self.cleaned_data.get("numer_lokalu")
        return value or None
