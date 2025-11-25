from django.shortcuts import render, redirect
from django.views import View
from aplikacjaTest.models import Oferta
from aplikacjaTest.forms.ofertaForm import OfertaForm
from django.contrib.auth.mixins import LoginRequiredMixin



# =======================================
#   LISTA WSZYSTKICH DOSTĘPNYCH OFERT
# =======================================
class OfertaListView(LoginRequiredMixin,View):
  
    def get(self, request):
        oferty = Oferta.objects.all()  # możesz dodać filtr tylko publiczne
        return render(request, "oferta/oferta_lista.html", {"oferty": oferty})
