from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages

def redirect_homepage(request):
    return redirect('home')

class HomePageView(TemplateView):
    template_name = "tweetApp/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'success_registration' in self.request.GET and self.request.GET['success_registration'] == "t":
            messages.add_message(self.request, messages.SUCCESS, 'Successful Registration. You can now login.')
        return context


