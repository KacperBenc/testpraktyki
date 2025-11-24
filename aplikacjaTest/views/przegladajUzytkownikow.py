from django.shortcuts import render, redirect
from django.views import View
from aplikacjaTest.models import Uzytkownik



# =======================================
#   LISTA WSZYSTKICH DOSTĘPNYCH OFERT
# =======================================
class UzytkownikListView(View):
    def get(self, request):
        uzytkownicy = Uzytkownik.objects.all()  # możesz dodać filtr tylko publiczne
        return render(request, "UzytkownicyLista.html", {"uzytkownicy": uzytkownicy})