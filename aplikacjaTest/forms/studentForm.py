from django import forms
from aplikacjaTest.models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["imie", "nazwisko", "data_urodzenia", "numer_indeksu"]