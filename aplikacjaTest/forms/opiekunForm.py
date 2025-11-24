from django import forms
from aplikacjaTest.models import OpiekunPraktyk

class OpiekunForm(forms.ModelForm):
    class Meta:
        model = OpiekunPraktyk
        exclude = ["uzytkownik"]