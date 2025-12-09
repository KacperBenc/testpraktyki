from django.urls import path
from aplikacjaTest.views.home import home
from aplikacjaTest.views.dodajOferte import OfertaCreateView
from aplikacjaTest.views.przegladajOferty import OfertaListView
from aplikacjaTest.views.rejestracja import rejestracja
from aplikacjaTest.views.przegladajUzytkownikow import UzytkownikListView
from aplikacjaTest.views.login import login_view
from aplikacjaTest.views.logout import logout_view
from aplikacjaTest.views.zgloszenie import (
    zgloszenie_na_oferte,
    moje_zgloszenia,
    bk_zgloszenia_lista,
    bk_zgloszenie_edytuj,
)

urlpatterns = [
    path("", home, name="home"),
    path("oferty/", OfertaListView.as_view(), name="lista_ofert"),
    path("oferty/nowa/", OfertaCreateView.as_view(), name="dodaj_oferte"),
    path("rejestracja/", rejestracja, name="rejestracja"),
    path("uzytkownicy/", UzytkownikListView.as_view(), name="przegladajUzytkownikow"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("oferty/<int:oferta_id>/zapisz/", zgloszenie_na_oferte, name="zgloszenie_na_oferte"),
    path("zgloszenia/moje/", moje_zgloszenia, name="moje_zgloszenia"),
    path("bk/zgloszenia/", bk_zgloszenia_lista, name="bk_zgloszenia_lista"),
    path("bk/zgloszenia/<int:pk>/", bk_zgloszenie_edytuj, name="bk_zgloszenie_edytuj"),
]
