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

    # Mapowanie formularzy zależnie od roli
    role_forms = {
        "Student": StudentForm,
        "Pracodawca": PracodawcaForm,
        "Opiekun Praktyk": OpiekunForm,
        "Pracownik BK": PracownikBKForm,
    }

    if request.method == "POST":
        main_form = RejestracjaForm(request.POST)
        adres_form = AdresForm(request.POST)

        role = request.POST.get("rola")
        extra_form_class = role_forms.get(role)
        extra_form = extra_form_class(request.POST) if extra_form_class else None

        # Czy rola wymaga adresu?
        role_requires_address = role in ["Student", "Pracodawca"]

        valid_main = main_form.is_valid()
        valid_address = (not role_requires_address) or adres_form.is_valid()
        valid_extra = (extra_form is None) or extra_form.is_valid()

        if valid_main and valid_address and valid_extra:

            # --- Zapis adresu (tylko jeśli wymagany) ---
            adres = adres_form.save() if role_requires_address else None

            # --- Zapis użytkownika ---
            user = main_form.save(commit=False)
            user.haslo = make_password(main_form.cleaned_data["haslo"])
            user.status_konta = None  # administrator ustawia później
            user.save()

            # --- Zapis powiązanej roli ---
            if extra_form:
                role_obj = extra_form.save(commit=False)
                role_obj.uzytkownik = user

                # jeśli model roli ma pole adresu — dodajemy
                if hasattr(role_obj, "adres") and adres is not None:
                    role_obj.adres = adres

                role_obj.save()

            messages.success(request, "Rejestracja przebiegła pomyślnie!")
            return redirect("home")

    else:
        main_form = RejestracjaForm()
        adres_form = AdresForm()
        extra_form = None

    # Formularze ról na potrzeby wyświetlania w template
    forms_map = {
        "student_form": StudentForm(),
        "pracodawca_form": PracodawcaForm(),
        "opiekun_form": OpiekunForm(),
        "pracownikbk_form": PracownikBKForm(),
        "adres_form": adres_form,
    }

    # Jeśli był POST i extra_form istnieje → chcemy pokazać jego błędy
    if request.method == "POST" and extra_form is not None:
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
        "adres_form": adres_form,
        **forms_map
    })