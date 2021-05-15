import json

from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest
from django.db.models import Count, Exists, OuterRef, Prefetch, Q, Subquery
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, TemplateView

from .forms import TweetForm
from .models import Comment, Follow, Like, Retweet, Tweet


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
            like = Like.objects.filter(tweet=OuterRef("pk"), user=self.request.user)
            follows = Follow.objects.filter(follower=user).values_list(
                "followed", flat=True
            )
            retweet_author = (
                Retweet.objects.filter(author__in=follows, tweet=OuterRef("pk"))
                .exclude(author=self.request.user)
                .values("author__username")
            )
            newsfeed = (
                Tweet.objects.filter(
                    Q(author__in=follows) | Q(retweets__author__in=follows)
                )
                .select_related("author", "author__profile")
                .annotate(
                    like_exists=Exists(like),
                    retweet_author=Subquery(retweet_author[:1]),
                )
                .order_by("-date")[:100]
            )
            context.update(
                {
                    "tweet_form": TweetForm(),
                    "newsfeed": newsfeed,
                    # "personnal_tweets": personnal_tweets,
                }
            )
        return context


class DetailTweetView(DetailView):
    model = Tweet
    template_name = "tweetApp/detail-tweet.html"

    def get_queryset(self):
        queryset = Tweet.objects.all().prefetch_related(
            Prefetch("comments", queryset=Comment.objects.order_by("-date")),
            "comments__author__profile",
            "author__profile",
        )
        if self.request.user.is_authenticated:
            like = Like.objects.filter(tweet=OuterRef("pk"), user=self.request.user)
            queryset = queryset.annotate(
                like_exists=Exists(like),
            )
        return queryset


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


@login_required
@require_POST
def commentView(request, id):
    tweet = Tweet.objects.get(id=id)
    content = json.loads(request.body).get("content")
    Comment.objects.create(content=content, tweet=tweet, author=request.user)
    return JsonResponse({"tweet": id, "created": "t"}, status=201)


class AccountView(View):
    @method_decorator(login_required)
    def get(self, request, username, *args, **kwargs):
        followed = get_user_model().objects.get(username=username)
        follow = Follow.objects.filter(followed=followed, follower=request.user)
        like = Like.objects.filter(tweet=OuterRef("pk"), user=request.user)
        account = (
            get_user_model()
            .objects.defer("is_staff", "is_superuser", "password", "is_active", "email")
            .select_related("profile")
            .prefetch_related(
                Prefetch(
                    "tweets",
                    Tweet.objects.order_by("-date").annotate(
                        Count("comments", distinct=True),
                        Count("likes", distinct=True),
                        Count("retweets", distinct=True),
                        like_exists=Exists(like),
                    ),
                )
            )
            .annotate(
                Count("followers", distinct=True),
                Count("follows", distinct=True),
                follow_exists=Exists(follow),
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
    obj, created = Like.objects.get_or_create(
        user=request.user, tweet=Tweet.objects.get(id=id)
    )
    if not created:
        obj.delete()
        return JsonResponse({"tweet": id, "created": "f"})
    return JsonResponse({"tweet": id, "created": "t"}, status=201)


@login_required
@require_POST
def retweetView(request, id):
    tweet = Tweet.objects.get(id=id)
    retweet = Retweet.objects.create(author=request.user, tweet=tweet)
    return JsonResponse({"tweet": id, "created": "t"}, status=201)


def searchView(request):
    search_param = request.GET.get("q", None)
    try:
        tweets = Tweet.objects.filter(content__icontains=search_param).prefetch_related(
            Prefetch("comments", queryset=Comment.objects.order_by("-date")),
            "comments__author__profile",
            "author__profile",
        )
        users = (
            get_user_model()
            .objects.filter(
                Q(username__icontains=search_param)
                | Q(first_name__icontains=search_param)
                | Q(last_name__icontains=search_param)
            )
            .select_related("profile")
            .annotate(Count("followers", distinct=True))
            .order_by("-followers__count")
        )
        if request.user.is_authenticated:
            like = Like.objects.filter(tweet=OuterRef("pk"), user=request.user)
            tweets = tweets.annotate(
                like_exists=Exists(like),
            )
            users = users.exclude(
                Q(id=request.user.id)
                | Q(followers__in=Follow.objects.filter(follower=request.user))
            )
    except:
        raise BadRequest("Bad request for searching.")
    return render(
        request,
        "tweetApp/search_results.html",
        {"tweets": tweets[:6], "users": users[:10]},
    )
