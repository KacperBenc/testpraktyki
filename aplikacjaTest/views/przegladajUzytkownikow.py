from django.shortcuts import render, redirect
from django.views import View
from aplikacjaTest.models import Uzytkownik
from django.contrib.auth.mixins import LoginRequiredMixin


# =======================================
#   LISTA WSZYSTKICH DOSTĘPNYCH OFERT
# =======================================
class UzytkownikListView(LoginRequiredMixin,View):
    def get(self, request):
        uzytkownicy = Uzytkownik.objects.all()  # możesz dodać filtr tylko publiczne
        uzytkownik = None
        if request.user.is_authenticated:
            try:
                uzytkownik = Uzytkownik.objects.get(django_user=request.user)
            except Uzytkownik.DoesNotExist:
                pass
        return render(request, "UzytkownicyLista.html", {"uzytkownicy": uzytkownicy,"uzytkownik": uzytkownik})