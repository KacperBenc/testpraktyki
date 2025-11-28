from django import forms
from aplikacjaTest.models import Zgloszenie


class ZgloszenieBKForm(forms.ModelForm):
    class Meta:
        model = Zgloszenie
        fields = ["status", "opiekun_praktyk"]
