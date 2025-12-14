from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from aplikacjaTest.models import Uzytkownik
from aplikacjaTest.forms.ofertaForm import UzytkownikFilterForm


class UzytkownikListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "aplikacjaTest.view_students"

    def get(self, request):
        qs = Uzytkownik.objects.all()
        form = UzytkownikFilterForm(request.GET or None)

        if form.is_valid():
            role = form.cleaned_data.get("rola")
            login = form.cleaned_data.get("login")
            email = form.cleaned_data.get("adres_mailowy")
            telefon = form.cleaned_data.get("numer_telefonu")

            if role:
                qs = qs.filter(rola__in=role)
            if login:
                qs = qs.filter(login__icontains=login)
            if email:
                qs = qs.filter(adres_mailowy__icontains=email)
            if telefon:
                qs = qs.filter(numer_telefonu__icontains=telefon)

        context = {
            "uzytkownicy": qs,
            "ofertaForm": form,
        }
        return render(request, "uzytkownicy_lista.html", context)
