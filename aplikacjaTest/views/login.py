from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from aplikacjaTest.models import Uzytkownik

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        login_input = request.POST.get("login")
        haslo = request.POST.get("haslo")

        try:
            profil = Uzytkownik.objects.select_related("django_user").get(login=login_input)
        except Uzytkownik.DoesNotExist:
            profil = None

        if profil is None:
            messages.error(request, "Niepoprawny login lub hasło.")
        elif profil.status_konta is False:  # konto zablokowane/nieaktywne
            messages.error(request, "Twoje konto jest nieaktywne. Skontaktuj się z administratorem.")
        else:
            user = authenticate(username=profil.django_user.username, password=haslo)
            if user is not None:
                login(request, user)
                messages.success(request, "Zalogowano pomyślnie.")
                return redirect("home")
            messages.error(request, "Niepoprawny login lub hasło.")

    return render(request, "login.html", {"is_login_page": True})
