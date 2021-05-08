from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Prefetch
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .forms import TweetForm
from .models import Follow, Tweet


def redirect_homepage(request):
    return redirect("home")


class HomePageView(TemplateView):
    template_name = "tweetApp/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (
            "success_registration" in self.request.GET
            and self.request.GET["success_registration"] == "t"
        ):
            messages.add_message(
                self.request,
                messages.SUCCESS,
                "Successful Registration. You can now login.",
            )
        elif "next" in self.request.GET:
            messages.add_message(
                self.request,
                messages.WARNING,
                "You need to be logged in to access to this page.",
            )
        if self.request.user.is_authenticated:
            user = self.request.user
            newsfeed = (
                Tweet.objects.filter(
                    author__in=Follow.objects.filter(followed=user).values_list(
                        "followed", flat=True
                    )
                )
                .select_related("author", "author__profile")
                .order_by("-date")[:100]
            )
            personnal_tweets = (
                Tweet.objects.filter(author=user)
                .select_related("author", "author__profile")
                .order_by("-date")[:100]
            )
            context.update(
                {
                    "tweet_form": TweetForm(),
                    "newsfeed": newsfeed,
                    "personnal_tweets": personnal_tweets,
                }
            )
        return context


@login_required
@require_POST
def tweetView(request):
    form = TweetForm(request.POST, request.FILES)
    if form.is_valid:
        tweet = form.save(commit=False)
        tweet.author = request.user
        tweet.save()
        return redirect(request.META["HTTP_REFERER"])
    messages.add_message(
        request,
        messages.WARNING,
        "The tweet could not be created!",
    )
    return redirect("home")


class AccountView(View):
    def get(self, request, username, *args, **kwargs):
        account = (
            get_user_model()
            .objects.defer("is_staff", "is_superuser", "password", "is_active", "email")
            .select_related("profile")
            .prefetch_related(Prefetch("tweets", Tweet.objects.order_by("-date")))
            .annotate(Count("followers"), Count("follows"))
            .get(username=username)
        )
        return render(request, "tweetApp/account-detail.html", {"account": account})

    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        return render(request, "tweetApp/account-detail.html")
