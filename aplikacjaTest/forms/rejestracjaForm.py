from django import forms
from aplikacjaTest.models import Uzytkownik

class RejestracjaForm(forms.ModelForm):
    haslo = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Uzytkownik
        fields = [
            "rola",
            "login",
            "haslo",
            "numer_telefonu",
            "adres_mailowy",
        ]