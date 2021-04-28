from django.urls import path, re_path
from .views import HomePageView, redirect_homepage, loginView, registerView

urlpatterns = [
    path('login/', loginView,  name='login'),
    path('register/', registerView,  name='register'),
    path('home/', HomePageView.as_view(), name='home'),
    path('', redirect_homepage)
]