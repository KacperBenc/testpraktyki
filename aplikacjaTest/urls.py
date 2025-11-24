from django.urls import path
from aplikacjaTest.views.home import home
from aplikacjaTest.views.dodajOferte import OfertaCreateView
from aplikacjaTest.views.przegladajOferty import OfertaListView
from aplikacjaTest.views.rejestracja import rejestracja
from aplikacjaTest.views.przegladajUzytkownikow import UzytkownikListView

urlpatterns = [
    path("", home, name="home"),
    path("oferty/", OfertaListView.as_view(), name="lista_ofert"),
    path("oferty/nowa/", OfertaCreateView.as_view(), name="dodaj_oferte"),
    path("rejestracja/", rejestracja, name="rejestracja"),
    path("uzytkownicy/", UzytkownikListView.as_view(),name="przegladajUzytkownikow" )
]