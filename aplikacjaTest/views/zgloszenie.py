from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from aplikacjaTest.forms.zgloszenieFrom import ZgloszenieForm
from aplikacjaTest.forms.zgloszenie_bk_form import ZgloszenieBKForm
from aplikacjaTest.models import Uzytkownik, Student, Zgloszenie, OpiekunPraktyk, PracownikBK


@login_required
def zgloszenie_nowe(request):
    uzytkownik = get_object_or_404(Uzytkownik, django_user=request.user)  # zalogowany user
    student = get_object_or_404(Student, uzytkownik=uzytkownik)

    if request.method == "POST":

        form = ZgloszenieForm(request.POST)

        if form.is_valid():
            zgloszenie = form.save(commit=False)

            zgloszenie.student = student

            zgloszenie.data_zgloszenia = timezone.now()

            zgloszenie.status = Zgloszenie.Status.ZGLOSZONE

            zgloszenie.save()

            return redirect("lista_ofert")
    else:

        form = ZgloszenieForm()

    context = {
        "form": form,
    }
    return render(request, "zgloszenie/zgloszenie_form.html", context)


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
    }
    return render(request, "bk/zgloszenia_lista.html", context)


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
    }
    return render(request, "bk/zgloszenie_edytuj.html", context)