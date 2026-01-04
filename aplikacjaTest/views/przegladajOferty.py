from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from aplikacjaTest.models import (
    Oferta,
    Uzytkownik,
    Student,
    Zgloszenie,
)


class OfertaListView(LoginRequiredMixin, View):
    """
    Lista wszystkich dostępnych ofert.
    """

    def get(self, request, *args, **kwargs):
        oferty = Oferta.objects.select_related("pracodawca").all()

        uzytkownik = Uzytkownik.objects.filter(django_user=request.user).first()
        user_role = uzytkownik.rola if uzytkownik else None

        moje_zgloszenia = set()

        if uzytkownik and uzytkownik.rola == Uzytkownik.Role.STUDENT:
            student = Student.objects.filter(uzytkownik=uzytkownik).first()
            if student:
                moje_zgloszenia = set(
                    Zgloszenie.objects
                    .filter(student=student)
                    .values_list("oferta_id", flat=True)
                )

        context = {
            "oferty": oferty,
            "moje_zgloszenia": moje_zgloszenia,
            "user_role": user_role,
        }
        return render(request, "oferta/oferta_lista.html", context)
