from django.shortcuts import redirect
from django.views.generic import TemplateView


def redirect_homepage(request):
    return redirect('home')

class HomePageView(TemplateView):
    template_name = "tweetApp/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


