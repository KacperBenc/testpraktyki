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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        allowed = {
            Uzytkownik.Role.STUDENT,
            Uzytkownik.Role.PRACODAWCA,
            Uzytkownik.Role.OPIEKUN,
        }

        choices = [
            (value, label)
            for value, label in Uzytkownik.Role.choices
            if value in allowed
        ]

        self.fields["rola"].choices = [("", "Wybierz rolę…")] + choices
        self.fields["rola"].required = True