from django.shortcuts import render, redirect
from django.views import View
from .models import Oferta
from .forms import OfertaForm


# =======================================
#   LISTA WSZYSTKICH DOSTĘPNYCH OFERT
# =======================================
class OfertaListView(View):
    def get(self, request):
        oferty = Oferta.objects.all()  # możesz dodać filtr tylko publiczne
        return render(request, "oferta/oferta_list.html", {"oferty": oferty})


# =======================================
#          DODAWANIE NOWEJ OFERTY
# =======================================
class OfertaCreateView(View):
    def get(self, request):
        form = OfertaForm()
        return render(request, "oferta/oferta_form.html", {"form": form})

    def post(self, request):
        form = OfertaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_ofert")

        return render(request, "oferta/oferta_form.html", {"form": form})