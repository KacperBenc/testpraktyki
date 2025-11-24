from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from aplikacjaTest.forms.rejestracjaForm import RejestracjaForm
from aplikacjaTest.forms.studentForm import StudentForm
from aplikacjaTest.forms.pracodawcaForm import PracodawcaForm
from aplikacjaTest.forms.opiekunForm import OpiekunForm
from aplikacjaTest.forms.pracownikBKForm import PracownikBKForm
from aplikacjaTest.forms.adresForm import AdresForm


def rejestracja(request):

    # mapowanie ról → formularze
    role_forms = {
        "Student": StudentForm,
        "Pracodawca": PracodawcaForm,
        "Opiekun Praktyk": OpiekunForm,
        "Pracownik BK": PracownikBKForm,
    }

    if request.method == "POST":

        # główny formularz użytkownika
        main_form = RejestracjaForm(request.POST, prefix="main")

        # formularz adresu
        adres_form = AdresForm(request.POST, prefix="adres")

        # wybrana rola
        role = request.POST.get("main-rola")
        extra_form_class = role_forms.get(role)
        extra_prefix = role.replace(" ", "_")

        extra_form = (
            extra_form_class(request.POST, prefix=extra_prefix)
            if extra_form_class else None
        )

        # role wymagające adresu
        requires_address = role in ["Student", "Pracodawca"]

        # WALIDACJA
        valid_main = main_form.is_valid()
        valid_address = (not requires_address) or adres_form.is_valid()
        valid_extra = (extra_form is None) or extra_form.is_valid()

        if valid_main and valid_address and valid_extra:

            # --- 1. Zapis adresu (jeśli wymagany)
            adres = adres_form.save() if requires_address else None

            # --- 2. Zapis użytkownika
            user = main_form.save(commit=False)
            user.haslo = make_password(main_form.cleaned_data["haslo"])
            user.status_konta = None
            user.save()

            # --- 3. Zapis obiektu roli
            if extra_form:
                role_obj = extra_form.save(commit=False)
                role_obj.uzytkownik = user

                # 🔥 zawsze przypisujemy adres Studentowi i Pracodawcy
                if role in ["Student", "Pracodawca"]:
                    role_obj.adres = adres

                role_obj.save()

            messages.success(request, "Rejestracja przebiegła pomyślnie!")
            return redirect("home")

        else:
            messages.error(request, "Popraw błędy i spróbuj ponownie.")

    else:
        main_form = RejestracjaForm(prefix="main")
        adres_form = AdresForm(prefix="adres")

    # formularze wyświetlane na stronie (puste lub z błędami)
    forms_map = {
        "student_form": StudentForm(prefix="Student"),
        "pracodawca_form": PracodawcaForm(prefix="Pracodawca"),
        "opiekun_form": OpiekunForm(prefix="Opiekun_Praktyk"),
        "pracownikbk_form": PracownikBKForm(prefix="Pracownik_BK"),
        "adres_form": adres_form,
    }

    return render(
        request,
        "rejestracja.html",
        {
            "form": main_form,
            **forms_map,
        },
    )
