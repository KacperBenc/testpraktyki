from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from aplikacjaTest.forms.zgloszenie_bk_form import ZgloszenieBKForm
from django.contrib import messages
from aplikacjaTest.models import (
    Uzytkownik,
    Student,
    Zgloszenie,
    Oferta,
    OpiekunPraktyk
)


@login_required
def zgloszenie_na_oferte(request, oferta_id):
    uzytkownik = get_object_or_404(Uzytkownik, django_user=request.user)

    # Tylko student może się zgłaszać
    if uzytkownik.rola != Uzytkownik.Role.STUDENT:
        messages.error(request, "Tylko student może zgłosić się na praktyki.")
        return redirect("lista_ofert")

    student = get_object_or_404(Student, uzytkownik=uzytkownik)
    oferta = get_object_or_404(Oferta, pk=oferta_id)

    if Zgloszenie.objects.filter(student=student, oferta=oferta).exists():
        messages.warning(request, "Już zgłosiłeś się na tę ofertę.")
        return redirect("lista_ofert")

    if request.method == "POST":
        Zgloszenie.objects.create(
            student=student,
            oferta=oferta,
            data_zgloszenia=timezone.now(),
            status=Zgloszenie.Status.ZGLOSZONE,
        )
        messages.success(request, "Pomyślnie zgłosiłeś się na ofertę.")
        return redirect("lista_ofert")

    return redirect("lista_ofert")


def moje_zgloszenia(request):
    uzytkownik = get_object_or_404(Uzytkownik, django_user=request.user)

    student = get_object_or_404(Student, uzytkownik=uzytkownik)

    zgloszenia = (
        Zgloszenie.objects
        .filter(student=student)
        .select_related("oferta", "oferta__pracodawca", "opiekun_praktyk")
        .order_by("-data_zgloszenia")
    )

    context = {
        "student": student,
        "zgloszenia": zgloszenia,
        "uzytkownik": uzytkownik,
    }

    return render(request, "zgloszenie/zgloszenie_lista_student.html", context)


@login_required
def bk_zgloszenia_lista(request):

    uzytkownik = get_object_or_404(
        Uzytkownik,
        django_user=request.user,
        rola=Uzytkownik.Role.PRACOWNIK_BK,
    )

    zgloszenia = (
        Zgloszenie.objects
        .select_related("oferta", "oferta__pracodawca", "student", "opiekun_praktyk")
        .order_by("-data_zgloszenia")
    )

    context = {
        "pracownik_bk": uzytkownik,
        "zgloszenia": zgloszenia,
        "uzytkownik": uzytkownik,
    }
    return render(request, "bk/zgloszenia_lista.html",  context)


@login_required
def bk_zgloszenie_edytuj(request, pk):

    uzytkownik = get_object_or_404(
        Uzytkownik,
        django_user=request.user,
        rola=Uzytkownik.Role.PRACOWNIK_BK,
    )

    zgloszenie = get_object_or_404(Zgloszenie, pk=pk)

    if request.method == "POST":
        form = ZgloszenieBKForm(request.POST, instance=zgloszenie)
        if form.is_valid():
            form.save()
            return redirect("bk_zgloszenia_lista")
    else:
        form = ZgloszenieBKForm(instance=zgloszenie)

    context = {
        "pracownik_bk": uzytkownik,
        "zgloszenie": zgloszenie,
        "form": form,
        "uzytkownik": uzytkownik,
    }

    return render(request, "bk/zgloszenie_edytuj.html", context)

@login_required
def opiekun_lista_studentow(request):
    uzytkownik = get_object_or_404(Uzytkownik, django_user=request.user)
    opiekun = get_object_or_404(OpiekunPraktyk, uzytkownik=uzytkownik)

    zgloszenia = Zgloszenie.objects.filter(opiekun_praktyk=opiekun).select_related("student", "oferta")

    context = {
        "zgloszenia": zgloszenia,
        "opiekun": opiekun,
        "uzytkownik": uzytkownik,
    }

    return render(
        request,
        "opiekun/lista_przypisanych_studentow.html",
        context
    )