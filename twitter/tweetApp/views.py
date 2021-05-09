from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Exists, Prefetch, OuterRef, Subquery
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .forms import TweetForm
from .models import Follow, Like, Tweet


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
            like = Like.objects.filter(tweet=OuterRef('pk'), user=self.request.user)
            newsfeed = (
                Tweet.objects.filter(
                    author__in=Follow.objects.filter(follower=user).values_list(
                        "followed", flat=True
                    )
                )
                .select_related("author", "author__profile")
                .annotate(Count("comments"), Count("likes"), Count("retweets"), like_exists=Exists(like),)
                .order_by("-date")[:100]
            )
            personnal_tweets = (
                Tweet.objects.filter(author=user)
                .select_related("author", "author__profile")
                .annotate(Count("comments"), Count("likes"), Count("retweets"), like_exists=Exists(like),)
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
        followed = get_user_model().objects.get(username=username)
        follow = Follow.objects.filter(followed=followed, follower=request.user)
        like = Like.objects.filter(tweet=OuterRef('pk'), user=request.user)
        account = (
            get_user_model()
            .objects.defer("is_staff", "is_superuser", "password", "is_active", "email")
            .select_related("profile")
            .prefetch_related(
                Prefetch(
                    "tweets",
                    Tweet.objects.order_by("-date").annotate(
                        Count("comments"), Count("likes"), Count("retweets"), like_exists=Exists(like),
                    ),
                )
            )
            .annotate(
                Count("followers"), Count("follows"), follow_exists=Exists(follow)
            )
            .get(username=username)
        )
        return render(request, "tweetApp/account-detail.html", {"account": account})

    @method_decorator(login_required)
    def post(self, request, username, *args, **kwargs):
        followed = get_user_model().objects.get(username=username)
        follow = Follow.objects.filter(followed=followed, follower=request.user)
        if follow.exists():
            follow.delete()
        else:
            Follow.objects.create(followed=followed, follower=request.user)
        return redirect("account-detail", username=username)

@login_required
@require_POST
def likeView(request, id):
    obj, created = Like.objects.get_or_create(user=request.user, tweet=Tweet.objects.get(id=id))
    if not created:
        obj.delete()
        return JsonResponse({'tweet': id, 'created': 'f'})
    return JsonResponse({'tweet': id, 'created': 't'}, status=201)
