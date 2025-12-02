from django import forms
from aplikacjaTest.models import Zgloszenie


class ZgloszenieBKForm(forms.ModelForm):
    class Meta:
        model = Zgloszenie
        fields = ["status", "opiekun_praktyk"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Domyślnie opiekun NIE jest wymagany
        self.fields["opiekun_praktyk"].required = False

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        opiekun = cleaned_data.get("opiekun_praktyk")

        # Jeśli status jest ZAAKCEPTOWANE → opiekun MUSI być podany
        if status == Zgloszenie.Status.ZAAKCEPTOWANE and not opiekun:
            self.add_error(
                "opiekun_praktyk",
                "Aby zaakceptować zgłoszenie, musisz wybrać opiekuna praktyk."
            )

        # Jeśli status ODRZUCONE → NIE wymagamy opiekuna i nawet go czyścimy
        if status == Zgloszenie.Status.ODRZUCONE:
            cleaned_data["opiekun_praktyk"] = None

        return cleaned_data
