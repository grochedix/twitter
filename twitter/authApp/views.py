import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.views.generic.edit import UpdateView

from .forms import ProfileForm


@require_POST
def loginView(request):
    if request.is_ajax():
        data = json.loads(request.body)
        user = authenticate(**data)
        if user is not None:
            login(request, user)
            return JsonResponse({"error": "None"}, status=200)
        else:
            return JsonResponse(
                {"error": "The combination of Username/Password is not correct."},
                status=400,
            )


@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")


@require_POST
def registerView(request):
    if request.is_ajax():
        data = json.loads(request.body)
        form = UserCreationForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({"error": "None"}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)


@login_required
def profileView(request):
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, "authApp/profile.html", {"form": profile_form})
