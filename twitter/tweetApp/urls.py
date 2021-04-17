from django.urls import path, re_path
from .views import HomePageView

urlpatterns = [
    re_path(r'(home)?', HomePageView.as_view(), name='home'),
]