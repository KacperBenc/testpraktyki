from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from aplikacjaTest.models import Uzytkownik
from aplikacjaTest.forms.ofertaForm import UzytkownikFilterForm


class UzytkownikListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "aplikacjaTest.view_students"

    def get(self, request):
        qs = (
            Uzytkownik.objects
            .select_related(
                "student__adres__miasto",
                "student__adres__kraj",
                "pracodawca__adres__miasto",
                "pracodawca__adres__kraj",
                "opiekunpraktyk",
                "pracownikbk",
            )
        )

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

        # przygotowanie atrybutów jak w widoku `profile`
        for u in qs:
            u.student_rel = getattr(u, "student", None)
            u.pracodawca_rel = getattr(u, "pracodawca", None)
            u.opiekun_rel = getattr(u, "opiekunpraktyk", None)
            u.pracownik_bk_rel = getattr(u, "pracownikbk", None)

            if u.student_rel:
                u.adres_rel = u.student_rel.adres
            elif u.pracodawca_rel:
                u.adres_rel = u.pracodawca_rel.adres
            elif u.opiekun_rel:
                u.adres_rel = u.opiekun_rel.adres
            elif u.pracownik_bk_rel:
                u.adres_rel = u.pracownik_bk_rel.adres

        context = {
            "uzytkownicy": qs,
            "ofertaForm": form,
        }
        return render(request, "uzytkownicy_lista.html", context)