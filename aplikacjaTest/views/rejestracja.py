from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from aplikacjaTest.forms.rejestracjaForm import RejestracjaForm
from aplikacjaTest.forms.studentForm import StudentForm
from aplikacjaTest.forms.pracodawcaForm import PracodawcaForm
from aplikacjaTest.forms.opiekunForm import OpiekunForm
from aplikacjaTest.forms.pracownikBKForm import PracownikBKForm
from aplikacjaTest.forms.adresForm import AdresForm


def rejestracja(request):

    role_forms = {
        "Student": StudentForm,
        "Pracodawca": PracodawcaForm,
        "Opiekun Praktyk": OpiekunForm,
        "Pracownik BK": PracownikBKForm,
    }

    if request.method == "POST":

        main_form = RejestracjaForm(request.POST, prefix="main")
        adres_form = AdresForm(request.POST, prefix="adres")

        role = request.POST.get("main-rola")
        extra_form_class = role_forms.get(role)

        extra_form = (
            extra_form_class(request.POST, prefix=role.replace(" ", "_"))
            if extra_form_class else None
        )

        requires_address = role in ["Student", "Pracodawca"]

        valid_main = main_form.is_valid()
        valid_address = (not requires_address) or adres_form.is_valid()
        valid_extra = (extra_form is None) or extra_form.is_valid()

        if valid_main and valid_address and valid_extra:

            # 1. Najpierw zapis adresu, jeśli wymagany
            adres = adres_form.save() if requires_address else None

            # 2. Tworzymy konto Django
            raw_password = main_form.cleaned_data["haslo"]

            django_user = User.objects.create_user(
                username=main_form.cleaned_data["login"],
                email=main_form.cleaned_data["adres_mailowy"],
                password=raw_password
            )

            # 3. Zapis użytkownika w twojej tabeli
            user = main_form.save(commit=False)

            # kopiujemy hash hasła z Django
            user.haslo = django_user.password
            user.save()

            # 4. Zapis obiektu roli
            if extra_form:
                role_obj = extra_form.save(commit=False)
                role_obj.uzytkownik = user

                # student/pracodawca zawsze muszą mieć adres
                if role in ["Student", "Pracodawca"]:
                    role_obj.adres = adres

                role_obj.save()

            messages.success(request, "Rejestracja przebiegła pomyślnie!")
            return redirect("home")

        messages.error(request, "Popraw błędy w formularzu.")

    else:
        main_form = RejestracjaForm(prefix="main")
        adres_form = AdresForm(prefix="adres")

    return render(
        request,
        "rejestracja.html",
        {
            "form": main_form,
            "student_form": StudentForm(prefix="Student"),
            "pracodawca_form": PracodawcaForm(prefix="Pracodawca"),
            "opiekun_form": OpiekunForm(prefix="Opiekun_Praktyk"),
            "pracownikbk_form": PracownikBKForm(prefix="Pracownik_BK"),
            "adres_form": adres_form,
        },
    )
