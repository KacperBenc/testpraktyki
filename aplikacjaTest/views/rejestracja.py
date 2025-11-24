from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from aplikacjaTest.forms.rejestracjaForm import RejestracjaForm

def rejestracja(request):
    if request.method == "POST":
        form = RejestracjaForm(request.POST)
        if form.is_valid():
            u = form.save(commit=False)
            u.haslo = make_password(form.cleaned_data["haslo"])  # HASH
            u.save()
            return redirect("lista_ofert")
    else:
        form = RejestracjaForm()

    return render(request, "rejestracja.html", {"form": form})