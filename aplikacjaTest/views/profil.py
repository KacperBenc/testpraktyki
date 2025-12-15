from django.views.generic import DetailView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.db import transaction
from django.contrib import messages

from aplikacjaTest.models import Uzytkownik
from aplikacjaTest.forms.profilEdycjaForm import (
    UzytkownikForm, AdresForm,
    StudentForm, PracodawcaForm,
    OpiekunForm, PracownikBKForm,
)


class CanEditProfileMixin(UserPassesTestMixin):
    """
    pracownik_bk: może edytować każdy profil
    inni: tylko swój własny
    """

    def is_pracownik_bk(self, user):
        # user = django.contrib.auth.models.User
        uzytkownik = getattr(user, "uzytkownik", None)  # odwrotna relacja z OneToOneField
        if uzytkownik is None:
            return False
        return uzytkownik.rola == Uzytkownik.Role.PRACOWNIK_BK

    def test_func(self):
        # obiekt profilu, który edytujemy (Uzytkownik)
        uzytkownik_obj = self.get_object()

        # aktualnie zalogowany django.contrib.auth.models.User
        user = self.request.user

        # pracownik BK – pełny dostęp
        if self.is_pracownik_bk(user):
            return True

        # inni – tylko własny profil
        uzytkownik = getattr(user, "uzytkownik", None)
        return uzytkownik is not None and uzytkownik.pk == uzytkownik_obj.pk


class CanViewProfileMixin(UserPassesTestMixin):
    def is_pracownik_bk(self, user):
        uzytkownik = getattr(user, "uzytkownik", None)
        if uzytkownik is None:
            return False
        return uzytkownik.rola == Uzytkownik.Role.PRACOWNIK_BK

    def test_func(self):
        uzytkownik_obj = self.get_object()
        user = self.request.user

        if self.is_pracownik_bk(user):
            return True

        uzytkownik = getattr(user, "uzytkownik", None)
        return uzytkownik is not None and uzytkownik.pk == uzytkownik_obj.pk



class UzytkownikDetailView(LoginRequiredMixin, CanViewProfileMixin, DetailView):
    model = Uzytkownik
    template_name = "uzytkownik/profil.html"
    context_object_name = "uzytkownik"
    permission_required = "aplikacjaTest.view_user_profile"  # dostosuj do swoich perms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uzytkownik = self.object

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

        context.update(
            {
                "student": student,
                "pracodawca": pracodawca,
                "opiekun": opiekun,
                "pracownik_bk": pracownik_bk,
                "adres": adres,
            }
        )
        return context

class UzytkownikUpdateView(LoginRequiredMixin, CanEditProfileMixin,UpdateView):
    model = Uzytkownik
    form_class = UzytkownikForm           # główny formularz
    template_name = "uzytkownik/profil_edycja.html"
    context_object_name = "uzytkownik"
    permission_required = "aplikacjaTest.change_user_profile"  # dostosuj

    def _get_role_data(self, uzytkownik):
        student = getattr(uzytkownik, "student", None)
        pracodawca = getattr(uzytkownik, "pracodawca", None)
        opiekun = getattr(uzytkownik, "opiekunpraktyk", None)
        pracownik_bk = getattr(uzytkownik, "pracownikbk", None)

        if student:
            return student.adres, StudentForm, student
        elif pracodawca:
            return pracodawca.adres, PracodawcaForm, pracodawca
        elif opiekun:
            return opiekun.adres, OpiekunForm, opiekun
        elif pracownik_bk:
            return pracownik_bk.adres, PracownikBKForm, pracownik_bk
        return None, None, None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uzytkownik = self.object

        adres, role_form_class, role_instance = self._get_role_data(uzytkownik)

        # jeśli formularze już są w kwargs (po POST), użyj ich
        uzytkownik_form = kwargs.get("uzytkownik_form") or UzytkownikForm(instance=uzytkownik)
        adres_form = kwargs.get("adres_form") or (AdresForm(instance=adres) if adres else None)
        role_form = kwargs.get("role_form") or (
            role_form_class(instance=role_instance) if role_form_class else None
        )

        back_url = reverse("profil", kwargs={"pk": uzytkownik.pk})
        if self.request.GET.get("from") == "list":
            back_url = reverse("przegladajUzytkownikow")

        context.update(
            {
                "uzytkownik_form": uzytkownik_form,
                "adres_form": adres_form,
                "role_form": role_form,
                "back_url": back_url,
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        uzytkownik = self.object

        adres, role_form_class, role_instance = self._get_role_data(uzytkownik)

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

        messages.error(request, "Nie udało się zapisać zmian. Sprawdź formularz.")
        context = self.get_context_data(
            uzytkownik_form=uzytkownik_form,
            adres_form=adres_form,
            role_form=role_form,
        )
        return self.render_to_response(context)


class UzytkownikToggleAktywnoscView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "aplikacjaTest.change_user_status"

    def post(self, request, pk):
        uzytkownik = Uzytkownik.objects.get(pk=pk)
        uzytkownik.status_konta = not uzytkownik.status_konta
        uzytkownik.save(update_fields=["status_konta"])

        if uzytkownik.status_konta:
            messages.success(request, f"Konto użytkownika {uzytkownik.login} zostało aktywowane.")
        else:
            messages.success(request, f"Konto użytkownika {uzytkownik.login} zostało dezaktywowane.")

        return redirect(reverse("przegladajUzytkownikow"))

    def get(self, request, pk):
        return redirect("przegladajUzytkownikow")

