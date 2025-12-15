from django.urls import path
from aplikacjaTest.views.profil import (
    UzytkownikDetailView,
    UzytkownikUpdateView,
    UzytkownikToggleAktywnoscView,
)
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
    przypisane_zgloszenia
)

urlpatterns = [
    path("", home, name="home"),
    path("oferty/", OfertaListView.as_view(), name="lista_ofert"),
    path("oferty/nowa/", OfertaCreateView.as_view(), name="dodaj_oferte"),
    path("rejestracja/", rejestracja, name="rejestracja"),
    path("profil/<int:pk>", UzytkownikDetailView.as_view(), name="profil"),
    path("profil/<int:pk>/edycja", UzytkownikUpdateView.as_view(), name="profil_edycja"),
    path("profil/<int:pk>/toggle", UzytkownikToggleAktywnoscView.as_view(), name="uzytkownik_toggle_aktywnosc"),
    path("uzytkownicy/", UzytkownikListView.as_view(), name="przegladajUzytkownikow"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("oferty/<int:oferta_id>/zapisz/", zgloszenie_na_oferte, name="zgloszenie_na_oferte"),
    path("zgloszenia/moje/", moje_zgloszenia, name="moje_zgloszenia"),
    path("zgloszenia/przypisane/", przypisane_zgloszenia, name="przypisane_zgloszenia"),
    path("bk/zgloszenia/", bk_zgloszenia_lista, name="bk_zgloszenia_lista"),
    path("bk/zgloszenia/<int:pk>/", bk_zgloszenie_edytuj, name="bk_zgloszenie_edytuj"),
]
