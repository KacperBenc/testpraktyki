from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from aplikacjaTest.models import (
    Oferta,
    Uzytkownik,
    Student,
    Zgloszenie,
)


from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


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
        uzytkownik = Uzytkownik.objects.filter(django_user=request.user).first()
        user_role = uzytkownik.rola if uzytkownik else None

        # Filtrowanie ofert z uwzględnieniem dostępności
        if uzytkownik and uzytkownik.rola == Uzytkownik.Role.PRACOWNIK_BK:
            # Pracownik BK widzi wszystkie oferty
            oferty = Oferta.objects.select_related("pracodawca").all()
        elif uzytkownik and uzytkownik.rola == Uzytkownik.Role.PRACODAWCA:
            # Pracodawca widzi publiczne oferty + swoje niepubliczne
            oferty = Oferta.objects.select_related("pracodawca").filter(
                Q(dostepnosc_oferty=Oferta.Dostepnosc.PUBLICZNA)
                | Q(pracodawca__uzytkownik=uzytkownik)
            )
        elif uzytkownik and uzytkownik.rola == Uzytkownik.Role.STUDENT:
            # Student widzi publiczne oferty + swoje niepubliczne
            oferty = Oferta.objects.select_related("pracodawca").filter(
                Q(dostepnosc_oferty=Oferta.Dostepnosc.PUBLICZNA)
                | Q(pracodawca__uzytkownik=uzytkownik)
            )
        else:
            # Inni użytkownicy widzą tylko publiczne oferty
            oferty = Oferta.objects.select_related("pracodawca").filter(
                dostepnosc_oferty=Oferta.Dostepnosc.PUBLICZNA
            )

        moje_zgloszenia = set()

        if uzytkownik and uzytkownik.rola == Uzytkownik.Role.STUDENT:
            student = Student.objects.filter(uzytkownik=uzytkownik).first()
            if student:
                moje_zgloszenia = set(
                    Zgloszenie.objects.filter(student=student).values_list(
                        "oferta_id", flat=True
                    )
                )

        context = {
            "oferty": oferty,
            "moje_zgloszenia": moje_zgloszenia,
            "user_role": user_role,
        }
        return render(request, "oferta/oferta_lista.html", context)
