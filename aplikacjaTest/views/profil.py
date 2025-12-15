from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db import transaction
from django.contrib import messages

from aplikacjaTest.models import Uzytkownik
from django.shortcuts import render, get_object_or_404
from aplikacjaTest.models import Uzytkownik, Student, Pracodawca, OpiekunPraktyk, PracownikBK
from aplikacjaTest.forms.profilEdycjaForm import (
    UzytkownikForm, AdresForm,
    StudentForm, PracodawcaForm,
    OpiekunForm, PracownikBKForm,
)

def profile(request, pk):
    uzytkownik = get_object_or_404(Uzytkownik, pk=pk)

    student = getattr(uzytkownik, "student", None)
    pracodawca = getattr(uzytkownik, "pracodawca", None)
    opiekun = getattr(uzytkownik, "opiekunpraktyk", None)
    pracownik_bk = getattr(uzytkownik, "pracownikbk", None)

    adres = None
    if student:
        adres = student.adres
    elif pracodawca:
        adres = pracodawca.adres
    elif opiekun:
        adres = opiekun.adres
    elif pracownik_bk:
        adres = pracownik_bk.adres

    context = {
        "uzytkownik": uzytkownik,
        "student": student,
        "pracodawca": pracodawca,
        "opiekun": opiekun,
        "pracownik_bk": pracownik_bk,
        "adres": adres,
    }
    return render(request, "uzytkownik/profil.html", context)

def profile_edit(request, pk):
    uzytkownik = get_object_or_404(Uzytkownik, pk=pk)

    student = getattr(uzytkownik, "student", None)
    pracodawca = getattr(uzytkownik, "pracodawca", None)
    opiekun = getattr(uzytkownik, "opiekunpraktyk", None)
    pracownik_bk = getattr(uzytkownik, "pracownikbk", None)

    if student:
        adres = student.adres
        role_form_class = StudentForm
        role_instance = student
    elif pracodawca:
        adres = pracodawca.adres
        role_form_class = PracodawcaForm
        role_instance = pracodawca
    elif opiekun:
        adres = opiekun.adres
        role_form_class = OpiekunForm
        role_instance = opiekun
    elif pracownik_bk:
        adres = pracownik_bk.adres
        role_form_class = PracownikBKForm
        role_instance = pracownik_bk
    else:
        adres = None
        role_form_class = None
        role_instance = None

    if request.method == "POST":
        uzytkownik_form = UzytkownikForm(request.POST, instance=uzytkownik)
        adres_form = AdresForm(request.POST, instance=adres) if adres else None
        role_form = role_form_class(request.POST, instance=role_instance) if role_form_class else None

        forms_valid = uzytkownik_form.is_valid()
        if adres_form:
            forms_valid = forms_valid and adres_form.is_valid()
        if role_form:
            forms_valid = forms_valid and role_form.is_valid()

        if forms_valid:
            with transaction.atomic():
                uzytkownik_form.save()
                if adres_form:
                    adres_form.save()
                if role_form:
                    role = role_form.save(commit=False)
                    role.uzytkownik = uzytkownik
                    if hasattr(role, "adres") and adres_form:
                        role.adres = adres_form.instance
                    role.save()
            messages.success(request, "Profil został zaktualizowany.")
            return redirect(reverse("profil", kwargs={"pk": uzytkownik.pk}))
        else:
            messages.error(request, "Nie udało się zapisać zmian. Sprawdź formularz.")
    else:
        uzytkownik_form = UzytkownikForm(instance=uzytkownik)
        adres_form = AdresForm(instance=adres) if adres else None
        role_form = role_form_class(instance=role_instance) if role_form_class else None

    back_url = reverse("profil", kwargs={"pk": uzytkownik.pk})
    if request.GET.get("from") == "list":
        back_url = reverse("przegladajUzytkownikow")  # nazwa URL listy użytkowników

    context = {
        "uzytkownik": uzytkownik,
        "uzytkownik_form": uzytkownik_form,
        "adres_form": adres_form,
        "role_form": role_form,
        "back_url": back_url,
    }
    return render(request, "uzytkownik/profil_edycja.html", context)


def uzytkownik_deaktywuj(request, pk):
    if request.method != "POST":
        return redirect("przegladajUzytkownikow")

    uzytkownik = get_object_or_404(Uzytkownik, pk=pk)

    uzytkownik.status_konta = False
    uzytkownik.save(update_fields=["status_konta"])

    messages.success(request, f"Konto użytkownika {uzytkownik.login} zostało dezaktywowane.")
    return redirect(reverse("przegladajUzytkownikow"))

def uzytkownik_toggle_aktywnosc(request, pk):
    if request.method != "POST":
        return redirect("przegladajUzytkownikow")

    uzytkownik = get_object_or_404(Uzytkownik, pk=pk)

    # przełączamy boolean
    uzytkownik.status_konta = not uzytkownik.status_konta
    uzytkownik.save(update_fields=["status_konta"])

    if uzytkownik.status_konta:
        messages.success(
            request,
            f"Konto użytkownika {uzytkownik.login} zostało aktywowane."
        )
    else:
        messages.success(
            request,
            f"Konto użytkownika {uzytkownik.login} zostało dezaktywowane."
        )

    return redirect(reverse("przegladajUzytkownikow"))