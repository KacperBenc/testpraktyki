from django import forms
from aplikacjaTest.models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ["uzytkownik"]