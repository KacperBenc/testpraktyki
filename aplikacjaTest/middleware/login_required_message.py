from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.urls import resolve


class LoginRequiredMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Jeśli użytkownik niezalogowany i ścieżka wymaga logowania
        if not request.user.is_authenticated and request.path not in [
            settings.LOGIN_URL,
            "/",
            "/rejestracja/",  # miejsca które mają być dostępne bez logowania
            "/admin/",
        ] and not request.path.startswith("/static/"):
            messages.error(request, "Aby oglądać tę stronę musisz być zalogowany!")
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        return self.get_response(request)
