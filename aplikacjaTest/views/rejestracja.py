from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from aplikacjaTest.forms.rejestracjaForm import RejestracjaForm
from aplikacjaTest.forms.studentForm import StudentForm
from aplikacjaTest.forms.pracodawcaForm import PracodawcaForm
from aplikacjaTest.forms.opiekunForm import OpiekunForm
from aplikacjaTest.forms.pracownikBKForm import PracownikBKForm
from aplikacjaTest.forms.adresForm import AdresForm

from aplikacjaTest.models import Adres


def rejestracja(request):

    role_forms = {
        "Student": StudentForm,
        "Pracodawca": PracodawcaForm,
        "Opiekun Praktyk": OpiekunForm,
        "Pracownik BK": PracownikBKForm,
    }

    if request.method == "POST":

        # --- główny formularz ---
        main_form = RejestracjaForm(request.POST, prefix="main")

        # --- adres (zawsze prefix, ukrywanie jest tylko JS) ---
        adres_form = AdresForm(request.POST, prefix="adres")

        # --- rola ---
        role = request.POST.get("main-rola")
        extra_form_class = role_forms.get(role)

        extra_prefix = role.replace(" ", "_") if extra_form_class else None
        extra_form = (
            extra_form_class(request.POST, prefix=extra_prefix)
            if extra_form_class else None
        )

        # Czy ta rola wymaga adresu?
        role_requires_address = role in ["Student", "Pracodawca"]

        valid_main = main_form.is_valid()
        valid_address = (not role_requires_address) or adres_form.is_valid()
        valid_extra = (extra_form is None) or extra_form.is_valid()

        if valid_main and valid_address and valid_extra:

            # Zapis adresu
            adres = adres_form.save() if role_requires_address else None

            # Zapis użytkownika
            user = main_form.save(commit=False)
            user.haslo = make_password(main_form.cleaned_data["haslo"])
            user.status_konta = None
            user.save()

            # Zapis roli
            if extra_form:
                role_obj = extra_form.save(commit=False)
                role_obj.uzytkownik = user

                if hasattr(role_obj, "adres") and adres is not None:
                    role_obj.adres = adres

                role_obj.save()

            messages.success(request, "Rejestracja przebiegła pomyślnie!")
            return redirect("home")

    else:
        main_form = RejestracjaForm(prefix="main")
        adres_form = AdresForm(prefix="adres")

    # Formularze wstępne (GET)
    forms_map = {
        "student_form": StudentForm(prefix="Student"),
        "pracodawca_form": PracodawcaForm(prefix="Pracodawca"),
        "opiekun_form": OpiekunForm(prefix="Opiekun_Praktyk"),
        "pracownikbk_form": PracownikBKForm(prefix="Pracownik_BK"),
        "adres_form": adres_form,
    }

    # Jeśli były błędy w extra_form → chcemy pokazać je na stronie
    if request.method == "POST":
        if role == "Student":
            forms_map["student_form"] = extra_form
        elif role == "Pracodawca":
            forms_map["pracodawca_form"] = extra_form
        elif role == "Opiekun Praktyk":
            forms_map["opiekun_form"] = extra_form
        elif role == "Pracownik BK":
            forms_map["pracownikbk_form"] = extra_form

    return render(request, "rejestracja.html", {
        "form": main_form,
        **forms_map,
    })
