from django.shortcuts import render
from aplikacjaTest.models import Uzytkownik


def home(request):
    uzytkownik = None
    if request.user.is_authenticated:
        try:
            uzytkownik = Uzytkownik.objects.get(django_user=request.user)
        except Uzytkownik.DoesNotExist:
            pass

        print(request.user, request.user.is_authenticated, request.user.username)

    return render(request, "home.html", {"uzytkownik": uzytkownik})
