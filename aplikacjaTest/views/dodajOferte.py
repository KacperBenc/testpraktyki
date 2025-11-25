from django.shortcuts import render, redirect
from django.views import View
from aplikacjaTest.models import Oferta
from aplikacjaTest.forms.ofertaForm import OfertaForm
from django.contrib.auth.mixins import LoginRequiredMixin



# =======================================
#          DODAWANIE NOWEJ OFERTY
# =======================================
class OfertaCreateView(LoginRequiredMixin,View):
    
    def get(self, request):
        form = OfertaForm()
        return render(request, "oferta/oferta_dodaj.html", {"form": form})
    
    def post(self, request):
        form = OfertaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_ofert")

        return render(request, "oferta/oferta_dodaj.html", {"form": form})