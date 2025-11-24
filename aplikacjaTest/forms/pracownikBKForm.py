from django import forms
from aplikacjaTest.models import PracownikBK

class PracownikBKForm(forms.ModelForm):
    class Meta:
        model = PracownikBK
        fields = ["imie", "nazwisko"]