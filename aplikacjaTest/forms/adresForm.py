from django import forms
from aplikacjaTest.models import Adres, Kraj


class AdresForm(forms.ModelForm):
    # zamiast FK do Miasto — pole tekstowe
    miasto_nazwa = forms.CharField(
        label="Miasto",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Wpisz lub wybierz miasto",
                "list": "miasta_list",
            }
        ),
    )

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
        widgets = {
            "kraj": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Wpisz lub wybierz kraj",
                    "list": "kraje_list",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pobierz kraje przez ForeignKey
        self.istniejace_kraje = (
            Adres.objects.select_related("kraj")
            .values_list("kraj__nazwa", flat=True)
            .distinct()
            .order_by("kraj__nazwa")
        )

        # Pobierz miasta przez ForeignKey
        self.istniejace_miasta = (
            Adres.objects.select_related("miasto")
            .values_list("miasto__nazwa", flat=True)
            .distinct()
            .order_by("miasto__nazwa")
        )

    def clean_numer_lokalu(self):
        value = self.cleaned_data.get("numer_lokalu")
        return value or None
