from django.urls import path, re_path
from .views import HomePageView, redirect_homepage

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('', redirect_homepage)
]