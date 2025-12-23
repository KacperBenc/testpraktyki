from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from aplikacjaTest.forms.zgloszenie_bk_form import ZgloszenieBKForm
from django.contrib import messages
from aplikacjaTest.models import Uzytkownik, Student, Zgloszenie, Oferta, OpiekunPraktyk


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


@permission_required("aplikacjaTest.view_own_applications")
def moje_zgloszenia(request):
    uzytkownik = get_object_or_404(Uzytkownik, django_user=request.user)

    student = get_object_or_404(Student, uzytkownik=uzytkownik)

    zgloszenia = (
        Zgloszenie.objects.filter(student=student)
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
    # Bezpieczne wyszukiwanie użytkownika (TAKA SAMA LOGIKA)
    uzytkownik = Uzytkownik.objects.filter(django_user=request.user).first()
    if not uzytkownik or uzytkownik.rola != Uzytkownik.Role.PRACOWNIK_BK:
        messages.error(request, "Brak dostępu do panelu Pracownika BK.")
        return redirect("home")

    zgloszenia = Zgloszenie.objects.select_related(
        "oferta", "oferta__pracodawca", "student", "opiekun_praktyk"
    ).order_by("-data_zgloszenia")

    context = {
        "pracownik_bk": uzytkownik,
        "zgloszenia": zgloszenia,
    }
    return render(request, "bk/zgloszenia_lista.html", context)


@login_required
def bk_zgloszenie_edytuj(request, pk):
    # Bezpieczne wyszukiwanie użytkownika
    uzytkownik = Uzytkownik.objects.filter(django_user=request.user).first()
    if not uzytkownik:
        messages.error(
            request, "Brak profilu użytkownika. Skontaktuj się z administratorem."
        )
        return redirect("home")

    # Sprawdź uprawnienia: Pracownik BK lub Opiekun
    if uzytkownik.rola not in [Uzytkownik.Role.PRACOWNIK_BK, Uzytkownik.Role.OPIEKUN]:
        messages.error(request, "Brak dostępu do edycji zgłoszeń.")
        return redirect("home")

    zgloszenie = get_object_or_404(Zgloszenie, pk=pk)
    next_url = request.GET.get("next", "home")

    # Dodatkowa walidacja dla Opiekuna - może edytować tylko swoje zgłoszenia
    if uzytkownik.rola == Uzytkownik.Role.OPIEKUN:
        opiekun = OpiekunPraktyk.objects.filter(uzytkownik=uzytkownik).first()
        if not opiekun or zgloszenie.opiekun_praktyk != opiekun:
            messages.error(
                request, "Możesz edytować tylko zgłoszenia przypisane do Ciebie."
            )
            return redirect("przypisane_zgloszenia")

    # Obsługa formularza POST
    if request.method == "POST":
        form = ZgloszenieBKForm(
            request.POST,
            instance=zgloszenie,
            current_user=uzytkownik,
            current_zgloszenie=zgloszenie,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Status zgłoszenia został zaktualizowany.")

            # Redirect w zależności od roli
            if uzytkownik.rola == Uzytkownik.Role.PRACOWNIK_BK:
                return redirect(next_url or "bk_zgloszenia_lista")
            else:
                return redirect(next_url or "przypisane_zgloszenia")
    else:
        # Obsługa formularza GET
        form = ZgloszenieBKForm(
            instance=zgloszenie, current_user=uzytkownik, current_zgloszenie=zgloszenie
        )

    # Kontekst dla template
    # Po walidacji formularza (GET/POST):
    context = {
        "uzytkownik": uzytkownik,
        "zgloszenie": zgloszenie,
        "form": form,
        "rola": uzytkownik.rola,  # ✅ STRING, nie enum.name!
        "powrot_url": (
            "bk_zgloszenia_lista"
            if uzytkownik.rola == "PRACOWNIK_BK"
            else "przypisane_zgloszenia"
        ),
    }
    return render(request, "bk/zgloszenie_edytuj.html", context)


@login_required
def przypisane_zgloszenia(request):
    # Bezpieczne wyszukiwanie użytkownika (TAKA SAMA LOGIKA)
    uzytkownik = Uzytkownik.objects.filter(django_user=request.user).first()
    if not uzytkownik or uzytkownik.rola != Uzytkownik.Role.OPIEKUN:
        messages.error(request, "Brak dostępu do panelu Opiekuna.")
        return redirect("home")

    opiekun = OpiekunPraktyk.objects.filter(uzytkownik=uzytkownik).first()
    if not opiekun:
        messages.error(request, "Brak profilu opiekuna.")
        return redirect("home")

    zgloszenia = (
        Zgloszenie.objects.filter(opiekun_praktyk=opiekun)
        .select_related("oferta", "oferta__pracodawca", "student")
        .order_by("-data_zgloszenia")
    )
    for z in zgloszenia:
        if z.oferta and z.oferta.opis:
            z.opis_bez_dopelnienia = (
                z.oferta.opis[: z.oferta.opis.find(":")]
                if ":" in z.oferta.opis
                else z.oferta.opis
            )
        else:
            z.opis_bez_dopelnienia = ""

    context = {
        "opiekun": opiekun,
        "zgloszenia": zgloszenia,
    }
    return render(request, "zgloszenie/przypisane_zgloszenia_lista.html", context)
