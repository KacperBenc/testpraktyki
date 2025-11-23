from django.urls import path
from .views import OfertaListView, OfertaCreateView

urlpatterns = [
    path("oferty/", OfertaListView.as_view(), name="lista_ofert"),
    path("oferty/nowa/", OfertaCreateView.as_view(), name="dodaj_oferte"),
]