from django import forms
from django.core.exceptions import ValidationError
from aplikacjaTest.models import Adres, Kraj, Miasto


class ForeignKeyWithTextInput(forms.CharField):
    """Pole umożliwiające wpisywanie tekstu dla ForeignKey z autocomplete"""

    def __init__(self, model, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        """Konwertuje nazwę na instancję modelu lub tworzy nową"""
        if not value:
            return None

        value = value.strip()
        # Szukaj istniejącego obiektu (case-insensitive)
        obj = self.model.objects.filter(nazwa__iexact=value).first()

        if not obj:
            # Utwórz nowy obiekt, jeśli nie istnieje
            obj = self.model.objects.create(nazwa=value.title())

        return obj


class AdresForm(forms.ModelForm):
    kraj = ForeignKeyWithTextInput(
        model=Kraj,
        label="Kraj",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Wpisz lub wybierz kraj",
                "list": "kraje_list",
                "autocomplete": "off",
            }
        ),
    )

    miasto = ForeignKeyWithTextInput(
        model=Miasto,
        label="Miasto",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Wpisz lub wybierz miasto",
                "list": "miasta_list",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = Adres
        fields = [
            "kraj",
            "miasto",
            "ulica",
            "numer_budynku",
            "numer_lokalu",
            "kod_pocztowy",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pobierz istniejące kraje - bezpośrednio z modelu Kraj
        self.istniejace_kraje = (
            Kraj.objects.values_list("nazwa", flat=True).distinct().order_by("nazwa")
        )

        # Pobierz istniejące miasta - bezpośrednio z modelu Miasto
        self.istniejace_miasta = (
            Miasto.objects.values_list("nazwa", flat=True).distinct().order_by("nazwa")
        )

        # Ustaw początkowe wartości dla edycji
        if self.instance and self.instance.pk:
            if self.instance.kraj:
                self.fields["kraj"].initial = self.instance.kraj.nazwa
            if self.instance.miasto:
                self.fields["miasto"].initial = self.instance.miasto.nazwa

    def clean_numer_lokalu(self):
        value = self.cleaned_data.get("numer_lokalu")
        return value or None
