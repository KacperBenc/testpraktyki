from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        login_input = request.POST.get("login")
        haslo = request.POST.get("haslo")

        user = authenticate(username=login_input, password=haslo)

        if user is not None:
            login(request, user)
            messages.success(request, "Zalogowano pomyślnie.")
            return redirect("home")  # lub np. "lista_ofert"

        messages.error(request, "Niepoprawny login lub hasło.")

    return render(request, "login.html")