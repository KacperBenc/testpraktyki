from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from aplikacjaTest.models import Uzytkownik


class UzytkownikListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "aplikacjaTest.view_students"  # app_label + codename

    def get(self, request):
        uzytkownicy = Uzytkownik.objects.all()
        return render(request, "UzytkownicyLista.html", {"uzytkownicy": uzytkownicy})
