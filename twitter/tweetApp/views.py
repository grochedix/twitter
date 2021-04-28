from django.conf import settings
from django.contrib.auth import authenticate, login
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
    user = authenticate(request.POST)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    else:
        return JsonResponse({'error': "Wrong Authentication"})

@require_POST
def registerView(request):
    if request.method == "POST" and request.is_ajax():
        data = json.loads(request.body)
        form = RegisterForm(data)
        if form.is_valid():
            return JsonResponse({'error': 'None'}, status=200)
        else:
            return JsonResponse({'error': form.errors}, status=400)
    return redirect('home')
