from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
import json

from .forms import RegisterForm


def redirect_homepage(request):
    return redirect('home')

class HomePageView(TemplateView):
    template_name = "tweetApp/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration_form'] = RegisterForm()
        return context

@require_POST
def loginView(request):
    if request.is_ajax():
        data = json.loads(request.body)
        user = authenticate(**data)
        if user is not None:
            login(request, user)
            return JsonResponse({'error': 'None'}, status=200)
        else:
            return JsonResponse({'error': "The combination of Username/Password is not correct."}, status=400)

@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')

@require_POST
def registerView(request):
    if request.is_ajax():
        data = json.loads(request.body)
        form = RegisterForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({'error': 'None'}, status=200)
        else:
            return JsonResponse({'error': form.errors}, status=400)
