from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from aplikacjaTest.forms.rejestracjaForm import RejestracjaForm
from aplikacjaTest.forms.adresForm import AdresForm
from aplikacjaTest.forms.studentForm import StudentForm
from aplikacjaTest.forms.pracodawcaForm import PracodawcaForm
from aplikacjaTest.forms.opiekunForm import OpiekunForm
from aplikacjaTest.forms.pracownikBKForm import PracownikBKForm

from aplikacjaTest.models import Miasto


def rejestracja(request):
    role_forms = {
        "Student": StudentForm,
        "Pracodawca": PracodawcaForm,
        "Opiekun Praktyk": OpiekunForm,
        "Pracownik BK": PracownikBKForm,
    }

    if request.method == "POST":
        main_form = RejestracjaForm(request.POST, prefix="main", user=request.user)
        adres_form = AdresForm(request.POST, prefix="adres")

        role = request.POST.get("main-rola")
        extra_class = role_forms.get(role)
        extra_prefix = role.replace(" ", "_") if extra_class else None
        extra_form = (
            extra_class(request.POST, prefix=extra_prefix) if extra_class else None
        )

        requires_address = role in [
            "Student",
            "Pracodawca",
            "Opiekun Praktyk",
            "Pracownik BK",
        ]

        valid_main = main_form.is_valid()
        valid_address = (not requires_address) or adres_form.is_valid()
        valid_extra = (extra_form is None) or extra_form.is_valid()

        if valid_main and valid_address and valid_extra:

            # =====================================================
            # 1) Zapis ADRESU (dla ról, które go wymagają)
            # =====================================================
            adres_instance = None
            if requires_address:
                adres_instance = adres_form.save(commit=False)

                # Pola kraj i miasto są już obiektami po walidacji
                # nie trzeba ich manualnie wyszukiwać

                if not adres_instance.numer_lokalu:
                    adres_instance.numer_lokalu = None
                adres_instance.save()

            # =====================================================
            # 2) Zapis UŻYTKOWNIKA
            # =====================================================
            haslo_raw = main_form.cleaned_data["haslo"]

            django_user = User.objects.create_user(
                username=main_form.cleaned_data["login"],
                password=haslo_raw,
                email=main_form.cleaned_data["adres_mailowy"],
            )

            # >>> 2a) PRZYPISANIE GRUPY NA PODSTAWIE ROLI <<<
            role_to_group = {
                "Student": "student",
                "Pracodawca": "pracodawca",
                "Opiekun Praktyk": "opiekun",
                "Pracownik BK": "pracownikBK",
            }
            group_name = role_to_group.get(role)
            if group_name:
                try:
                    group = Group.objects.get(name=group_name)
                    django_user.groups.add(group)
                except Group.DoesNotExist:
                    pass

            user = main_form.save(commit=False)
            user.haslo = make_password(haslo_raw)
            user.django_user = django_user
            user.status_konta = None
            user.save()

            # =====================================================
            # 3) Zapis ROLI — Student/Pracodawca/Opiekun/BK
            # =====================================================
            if extra_form:
                role_obj = extra_form.save(commit=False)
                role_obj.uzytkownik = user

                if requires_address:
                    role_obj.adres = adres_instance

                role_obj.save()

            messages.success(request, "Rejestracja przebiegła pomyślnie!")
            return redirect("home")

        messages.error(request, "Popraw błędy formularza.")

    else:
        main_form = RejestracjaForm(prefix="main", user=request.user)
        adres_form = AdresForm(prefix="adres")
        extra_form = None
        role = None

    forms_map = {
        "student_form": StudentForm(prefix="Student"),
        "pracodawca_form": PracodawcaForm(prefix="Pracodawca"),
        "opiekun_form": OpiekunForm(prefix="Opiekun_Praktyk"),
        "pracownikbk_form": PracownikBKForm(prefix="Pracownik_BK"),
        "adres_form": adres_form,
    }

    if request.method == "POST" and extra_form is not None:
        if role == "Student":
            forms_map["student_form"] = extra_form
        elif role == "Pracodawca":
            forms_map["pracodawca_form"] = extra_form
        elif role == "Opiekun Praktyk":
            forms_map["opiekun_form"] = extra_form
        elif role == "Pracownik BK":
            forms_map["pracownikbk_form"] = extra_form

    return render(
        request,
        "rejestracja.html",
        {
            "form": main_form,
            **forms_map,
            "istniejace_kraje": adres_form.istniejace_kraje,
            "istniejace_miasta": adres_form.istniejace_miasta,
        },
    )
