from django import forms
from aplikacjaTest.models import Pracodawca

class PracodawcaForm(forms.ModelForm):
    class Meta:
        model = Pracodawca
        exclude = ["uzytkownik"]