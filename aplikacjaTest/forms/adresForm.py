from django import forms
from aplikacjaTest.models import Adres

class AdresForm(forms.ModelForm):
    class Meta:
        model = Adres
        fields = ["miasto", "kraj", "ulica", "numer_budynku", "numer_lokalu", "kod_pocztowy"]