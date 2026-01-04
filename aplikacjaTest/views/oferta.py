from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, View
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib import messages
from django.db import transaction

from aplikacjaTest.models import Oferta, Pracodawca, Uzytkownik
from aplikacjaTest.forms.ofertaForm import OfertaForm


class OfertaPermissionMixin(UserPassesTestMixin):
    """
    Bezpieczny mixin sprawdzający uprawnienia:
    - Pracownik BK: wymaga globalnego uprawnienia
    - Pracodawca: wymaga globalnego uprawnienia + własność oferty
    """

    def test_func(self):
        user = self.request.user

        if not user.is_authenticated:
            return False

        # Pobierz ofertę
        oferta = self.get_object()

        # Sprawdź uprawnienia Django
        permission = self.get_required_permission()
        if not user.has_perm(permission):
            return False

        # Jeśli Pracownik BK - dostęp do wszystkiego
        uzytkownik = getattr(user, "uzytkownik", None)
        if uzytkownik and uzytkownik.rola == Uzytkownik.Role.PRACOWNIK_BK:
            return True

        # Jeśli Pracodawca - tylko własne oferty
        if uzytkownik:
            try:
                pracodawca = Pracodawca.objects.get(uzytkownik=uzytkownik)
                return oferta.pracodawca.pk == pracodawca.pk
            except Pracodawca.DoesNotExist:
                return False

        return False

    def get_required_permission(self):
        """Override w klasach potomnych"""
        raise NotImplementedError


class CanManageOfferMixin(UserPassesTestMixin):
    """
    Pracownik BK: może edytować/usuwać każdą ofertę
    Pracodawca: tylko swoje oferty
    Student: tylko swoje oferty
    """

    def is_pracownik_bk(self, user):
        """Sprawdza czy użytkownik jest Pracownikiem BK"""
        uzytkownik = getattr(user, "uzytkownik", None)
        if uzytkownik is None:
            return False
        return uzytkownik.rola == Uzytkownik.Role.PRACOWNIK_BK

    def is_student(self, user):
        """Sprawdza czy użytkownik jest Studentem"""
        uzytkownik = getattr(user, "uzytkownik", None)
        if uzytkownik is None:
            return False
        return uzytkownik.rola == Uzytkownik.Role.STUDENT

    def test_func(self):
        """Sprawdza uprawnienia do zarządzania ofertą"""
        user = self.request.user

        # Pracownik BK – pełny dostęp
        if self.is_pracownik_bk(user):
            return True

        oferta = self.get_object()
        uzytkownik = getattr(user, "uzytkownik", None)

        if uzytkownik is None:
            return False

        # Pracodawca – tylko własne oferty
        try:
            pracodawca = Pracodawca.objects.get(uzytkownik=uzytkownik)
            return oferta.pracodawca.pk == pracodawca.pk
        except Pracodawca.DoesNotExist:
            pass

        # Student – tylko oferty, które sam stworzył
        # Zakładam, że dodasz pole 'utworzyl_uzytkownik' do modelu Oferta
        # lub sprawdzisz przez inny mechanizm (np. dodatkowa relacja)
        if self.is_student(user):
            # Opcja 1: jeśli masz pole utworzyl_uzytkownik w Oferta
            return (
                hasattr(oferta, "utworzyl_uzytkownik")
                and oferta.utworzyl_uzytkownik == uzytkownik
            )

            # Opcja 2: jeśli brak pola, możesz tymczasowo pozwolić na edycję wszystkich
            # return True

        return False


class OfertaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Oferta
    form_class = OfertaForm
    template_name = "oferta/oferta_dodaj.html"
    success_url = reverse_lazy("lista_ofert")
    permission_required = "aplikacjaTest.add_offer_portal"

    def get_form_kwargs(self):
        """Przekaż użytkownika do formularza"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oferta_form = kwargs.get("oferta_form") or OfertaForm(user=self.request.user)
        context.update(
            {
                "oferta_form": oferta_form,
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = None
        oferta_form = OfertaForm(request.POST, user=request.user)

        if oferta_form.is_valid():
            uzytkownik = getattr(request.user, "uzytkownik", None)
            is_pracownik_bk = False
            is_student = False

            if uzytkownik:
                is_pracownik_bk = uzytkownik.rola == Uzytkownik.Role.PRACOWNIK_BK
                is_student = uzytkownik.rola == Uzytkownik.Role.STUDENT

            # Pracownik BK - używa danych z formularza
            if is_pracownik_bk:
                with transaction.atomic():
                    oferta = oferta_form.save()
                    messages.success(request, "Oferta została pomyślnie utworzona.")
                    return redirect(reverse("lista_ofert"))

            # Student - wybiera pracodawcę i rodzaj zgłoszenia, dostępność automatycznie niepubliczna
            elif is_student:
                with transaction.atomic():
                    oferta = oferta_form.save(commit=False)
                    # Automatycznie ustaw dostępność na "Niepubliczna"
                    oferta.dostepnosc_oferty = Oferta.Dostepnosc.NIEPUBLICZNA
                    # Opcjonalnie: zapisz kto stworzył ofertę
                    # oferta.utworzyl_uzytkownik = uzytkownik
                    oferta.save()

                messages.success(request, "Oferta została pomyślnie utworzona.")
                return redirect(reverse("lista_ofert"))

            # Pracodawca - automatyczne przypisanie
            else:
                try:
                    pracodawca = Pracodawca.objects.get(
                        uzytkownik__django_user=request.user
                    )

                    with transaction.atomic():
                        oferta = oferta_form.save(commit=False)
                        # Automatycznie przypisz pracodawcę
                        oferta.pracodawca = pracodawca
                        # Automatycznie ustaw rodzaj zgłoszenia na "Praktyki"
                        oferta.rodzaj_zgloszenia = "Praktyki"
                        oferta.save()

                    messages.success(request, "Oferta została pomyślnie utworzona.")
                    return redirect(reverse("lista_ofert"))

                except Pracodawca.DoesNotExist:
                    messages.error(request, "Brak powiązanego profilu pracodawcy.")
                    return redirect(reverse("lista_ofert"))

        messages.error(request, "Nie udało się utworzyć oferty. Sprawdź formularz.")
        context = self.get_context_data(oferta_form=oferta_form)
        return self.render_to_response(context)


class OfertaEditView(
    LoginRequiredMixin, PermissionRequiredMixin, CanManageOfferMixin, UpdateView
):
    model = Oferta
    form_class = OfertaForm
    template_name = "oferta/oferta_edytuj.html"
    success_url = reverse_lazy("lista_ofert")
    permission_required = "aplikacjaTest.change_offer_portal"
    pk_url_kwarg = "oferta_id"
    context_object_name = "oferta"

    def get_form_kwargs(self):
        """Przekaż użytkownika do formularza"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oferta = self.object
        oferta_form = kwargs.get("oferta_form") or OfertaForm(
            instance=oferta, user=self.request.user
        )
        back_url = reverse("lista_ofert")
        context.update(
            {
                "oferta_form": oferta_form,
                "back_url": back_url,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        oferta = self.object
        oferta_form = OfertaForm(request.POST, instance=oferta, user=request.user)

        if oferta_form.is_valid():
            with transaction.atomic():
                saved_oferta = oferta_form.save(commit=False)
                # Dla pracodawców: zabezpiecz przed zmianą pracodawcy
                if not self.is_pracownik_bk(request.user):
                    saved_oferta.pracodawca = oferta.pracodawca
                    saved_oferta.rodzaj_zgloszenia = "Praktyki"
                saved_oferta.save()

            messages.success(request, "Oferta została zaktualizowana.")
            return redirect(reverse("lista_ofert"))

        messages.error(request, "Nie udało się zapisać zmian. Sprawdź formularz.")
        context = self.get_context_data(oferta_form=oferta_form)
        return self.render_to_response(context)

    def is_pracownik_bk(self, user):
        """Sprawdza czy użytkownik jest Pracownikiem BK"""
        uzytkownik = getattr(user, "uzytkownik", None)
        if uzytkownik is None:
            return False
        return uzytkownik.rola == Uzytkownik.Role.PRACOWNIK_BK


class OfertaDeleteView(LoginRequiredMixin, OfertaPermissionMixin, View):
    model = Oferta

    def get_required_permission(self):
        return "aplikacjaTest.delete_offer_portal"

    def get_object(self):
        oferta_id = self.kwargs.get("oferta_id")
        return get_object_or_404(Oferta, pk=oferta_id)

    def get(self, request, oferta_id):
        messages.warning(request, "Usuwanie oferty wymaga potwierdzenia.")
        return redirect(reverse("lista_ofert"))

    def post(self, request, oferta_id):
        oferta = self.get_object()
        oferta_info = str(oferta)

        try:
            oferta.delete()
            messages.success(request, f"Oferta '{oferta_info}' została usunięta.")

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse(
                    {
                        "success": True,
                        "message": f"Oferta '{oferta_info}' został usunięta.",
                    }
                )

            return redirect(reverse("lista_ofert"))
        except Exception as e:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": False, "error": str(e)}, status=500)

            messages.error(request, f"Wystąpił błąd podczas usuwania oferty: {str(e)}")
            return redirect(reverse("lista_ofert"))
