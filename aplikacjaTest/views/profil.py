from django.shortcuts import render, get_object_or_404
from aplikacjaTest.models import Uzytkownik

def profile(request, pk):
    uzytkownik = get_object_or_404(Uzytkownik, pk=pk)
    return render(request, "uzytkownik/profil.html", {"uzytkownik": uzytkownik})
