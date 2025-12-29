from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
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


class CanManageOfferMixin(UserPassesTestMixin):
    """
    Pracownik BK: może edytować/usuwać każdą ofertę
    Pracodawca: tylko swoje oferty
    """

    def is_pracownik_bk(self, user):
        """Sprawdza czy użytkownik jest Pracownikiem BK"""
        uzytkownik = getattr(user, "uzytkownik", None)
        if uzytkownik is None:
            return False
        return uzytkownik.rola == Uzytkownik.Role.PRACOWNIK_BK

    def test_func(self):
        """Sprawdza uprawnienia do zarządzania ofertą"""
        user = self.request.user

        # Pracownik BK – pełny dostęp
        if self.is_pracownik_bk(user):
            return True

        # Pracodawca – tylko własne oferty
        oferta = self.get_object()
        uzytkownik = getattr(user, "uzytkownik", None)

        if uzytkownik is None:
            return False

        try:
            pracodawca = Pracodawca.objects.get(uzytkownik=uzytkownik)
            return oferta.pracodawca.pk == pracodawca.pk
        except Pracodawca.DoesNotExist:
            return False


class OfertaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Oferta
    form_class = OfertaForm
    template_name = "oferta/oferta_dodaj.html"
    success_url = reverse_lazy("lista_ofert")
    permission_required = "aplikacjaTest.add_offer_portal"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oferta_form = kwargs.get("oferta_form") or OfertaForm()
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
        oferta_form = OfertaForm(request.POST)

        if oferta_form.is_valid():
            try:
                pracodawca = Pracodawca.objects.get(
                    uzytkownik__django_user=request.user
                )
                with transaction.atomic():
                    oferta = oferta_form.save(commit=False)
                    oferta.pracodawca = pracodawca
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oferta = self.object

        oferta_form = kwargs.get("oferta_form") or OfertaForm(instance=oferta)

        back_url = reverse("lista_ofert")

        context.update(
            {
                "oferta_form": oferta_form,
                "back_url": back_url,
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        oferta = self.object

        oferta_form = OfertaForm(request.POST, instance=oferta)

        if oferta_form.is_valid():
            with transaction.atomic():
                oferta_form.save()
            messages.success(request, "Oferta została zaktualizowana.")
            return redirect(reverse("lista_ofert"))

        messages.error(request, "Nie udało się zapisać zmian. Sprawdź formularz.")
        context = self.get_context_data(oferta_form=oferta_form)
        return self.render_to_response(context)


class OfertaDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, CanManageOfferMixin, View
):
    model = Oferta
    permission_required = "aplikacjaTest.delete_offer_portal"

    def get_object(self):
        """Pobiera obiekt oferty na podstawie oferta_id"""
        oferta_id = self.kwargs.get("oferta_id")
        return get_object_or_404(Oferta, pk=oferta_id)

    def get(self, request, oferta_id):
        oferta = self.get_object()
        context = {
            "oferta": oferta,
            "back_url": reverse("lista_ofert"),
        }
        return render(request, "oferta/oferta_usun.html", context)

    def post(self, request, oferta_id):
        oferta = self.get_object()
        oferta_info = str(oferta)
        oferta.delete()

        messages.success(request, f"Oferta '{oferta_info}' została usunięta.")
        return redirect(reverse("lista_ofert"))
