from django.shortcuts import redirect
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "tweetApp/homepage.html"
