from django import forms
from aplikacjaTest.models import Zgloszenie


class ZgloszenieForm(forms.ModelForm):

    class Meta:
        model = Zgloszenie
        fields = ["oferta"]
