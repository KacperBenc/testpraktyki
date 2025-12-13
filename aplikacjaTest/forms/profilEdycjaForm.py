# forms.py
from django import forms
from aplikacjaTest.models import Uzytkownik, Student, Pracodawca, OpiekunPraktyk, PracownikBK, Adres

class UzytkownikForm(forms.ModelForm):
    class Meta:
        model = Uzytkownik
        fields = ["numer_telefonu", "adres_mailowy"]

class AdresForm(forms.ModelForm):
    class Meta:
        model = Adres
        fields = ["kraj", "miasto", "ulica", "numer_budynku", "numer_lokalu", "kod_pocztowy"]

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["imie", "nazwisko", "data_urodzenia", "numer_indeksu"]

class PracodawcaForm(forms.ModelForm):
    class Meta:
        model = Pracodawca
        fields = ["imie_przedstawiciela", "nazwisko_przedstawiciela", "nazwa_firmy", "nip"]

class OpiekunForm(forms.ModelForm):
    class Meta:
        model = OpiekunPraktyk
        fields = ["imie", "nazwisko"]

class PracownikBKForm(forms.ModelForm):
    class Meta:
        model = PracownikBK
        fields = ["imie", "nazwisko"]
