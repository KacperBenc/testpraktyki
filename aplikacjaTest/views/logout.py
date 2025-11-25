from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def logout_view(request):
    logout(request)
    messages.info(request, "Wylogowano.")
    return redirect("login")