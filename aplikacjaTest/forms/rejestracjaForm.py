from django import forms
from aplikacjaTest.models import Uzytkownik

class RejestracjaForm(forms.ModelForm):
    haslo = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Uzytkownik
        fields = ["rola", "login", "haslo", "numer_telefonu", "adres_mailowy"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # domyślne role (rejestracja standardowa)
        allowed = {
            Uzytkownik.Role.STUDENT,
            Uzytkownik.Role.PRACODAWCA,
            Uzytkownik.Role.OPIEKUN,
        }

        # próba dojścia do Uzytkownik
        uzytkownik = None
        if user is not None and user.is_authenticated:
            uzytkownik = getattr(user, "uzytkownik", None)

        # jeśli zalogowany Uzytkownik ma rolę PRACOWNIK_BK
        if uzytkownik is not None and uzytkownik.rola == Uzytkownik.Role.PRACOWNIK_BK:
            allowed = {value for value, _ in Uzytkownik.Role.choices}

        choices = [
            (value, label)
            for value, label in Uzytkownik.Role.choices
            if value in allowed
        ]

        self.fields["rola"].choices = [("", "Wybierz rolę…")] + choices
        self.fields["rola"].required = True
