from django import forms
from aplikacjaTest.models import Zgloszenie, Uzytkownik


class ZgloszenieBKForm(forms.ModelForm):
    class Meta:
        model = Zgloszenie
        fields = ["status", "opiekun_praktyk"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
            "opiekun_praktyk": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        # Dodatkowe parametry dla blokady opiekuna
        self.current_user = kwargs.pop("current_user", None)
        self.current_zgloszenie = kwargs.pop("current_zgloszenie", None)

        super().__init__(*args, **kwargs)

        # Domyślnie opiekun NIE jest wymagany
        self.fields["opiekun_praktyk"].required = False

        # BLOKADA DLA OPIEKUNA - ukryj i zablokuj pole
        if self.current_user and self.current_user.rola == Uzytkownik.Role.OPIEKUN:
            self.fields["opiekun_praktyk"].disabled = True
            self.fields["opiekun_praktyk"].widget.attrs["readonly"] = True
            # Ustaw ukryte pole z bieżącą wartością
            if self.current_zgloszenie and self.current_zgloszenie.opiekun_praktyk:
                self.initial["opiekun_praktyk"] = (
                    self.current_zgloszenie.opiekun_praktyk
                )

    def clean_opiekun_praktyk(self):
        """Blokada zmiany opiekuna przez opiekuna"""
        opiekun = self.cleaned_data.get("opiekun_praktyk")

        # Opiekun NIE MOŻE zmieniać przypisania
        if (
            self.current_user
            and self.current_user.rola == Uzytkownik.Role.OPIEKUN
            and self.current_zgloszenie
            and self.current_zgloszenie.opiekun_praktyk
        ):

            # Sprawdź czy próbowano zmienić opiekuna
            if opiekun != self.current_zgloszenie.opiekun_praktyk:
                raise forms.ValidationError(
                    "Nie możesz przypisać zgłoszenia innemu opiekunowi. "
                    "Skontaktuj się z Biurem Karier."
                )
            # Zwróć oryginalnego opiekuna
            return self.current_zgloszenie.opiekun_praktyk

        return opiekun

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        opiekun = cleaned_data.get("opiekun_praktyk")

        # Jeśli status jest ZAAKCEPTOWANE → opiekun MUSI być podany
        if status == Zgloszenie.Status.ZAAKCEPTOWANE and not opiekun:
            self.add_error(
                "opiekun_praktyk",
                "Aby zaakceptować zgłoszenie, musisz wybrać opiekuna praktyk.",
            )

        # Jeśli status ODRZUCONE → NIE wymagamy opiekuna i nawet go czyścimy
        if status == Zgloszenie.Status.ODRZUCONE:
            cleaned_data["opiekun_praktyk"] = None

        return cleaned_data
