from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from aplikacjaTest.models import Oferta
from aplikacjaTest.forms.ofertaForm import OfertaForm


class OfertaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Oferta
    form_class = OfertaForm
    template_name = "oferta/oferta_dodaj.html"
    success_url = reverse_lazy("lista_ofert")

    permission_required = "aplikacjaTest.add_offer_portal"
