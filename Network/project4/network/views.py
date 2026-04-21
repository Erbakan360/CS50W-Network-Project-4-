from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import User, Posts, Like, Follower

@login_required
def index(request):
    all_posts = Posts.objects.all().order_by("id").reverse()

    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "all_posts": all_posts,
        "Posts": page_obj,
        })


@login_required
def New_Post(request):
    if request.method == "POST":
        Postbody = request.POST.get("Post_body")

        if Postbody == None or Postbody == "":
            Error = "Cannot leave post field blank"
        else:
            Error = None
            Post = Posts(
                user = User.objects.get(username = request.user),
                content = Postbody,
                time = datetime.today().replace(microsecond=0),
            )
            Post.save()
    return redirect("index")

@login_required
def Likes(request): # I could figure out how to do it with javaScript :(
    ID = int(request.POST.get("id"))
    user = User.objects.get(username = request.user)
    Post = Posts.objects.get(id = ID)
    if len(Like.objects.all().filter(post = Post).filter(liked_users = user)) == 0:
        Post.like = Post.like + 1
        Post.save()
        if len(Like.objects.all().filter(post= Post)) == 0:
            lik = Like(post = Post)
            lik.save()
        lik = Like.objects.get(post= Post)
        
        lik.liked_users.set(User.objects.all().filter(username = request.user))
        lik.save()
    else:
        Post.like = Post.like - 1
        Post.save()
        lik = Like.objects.all().filter(liked_users = user).filter(post = Post)
        lik.delete()

    return redirect("index")

@login_required
def Edit(request):
    if request.method == "POST":
        ID = int(request.POST.get("id"))
        Edit_post = Posts.objects.get(id = ID)
        return render(request, "network/Edit.html",{"Edit":Edit_post})

@login_required
def Save_Edit(request):
    if request.method == "POST":
        ID = int(request.POST.get("id"))
        Edited = request.POST.get("Edited")
        Post = Posts.objects.get(id = ID)
        Post.content = Edited
        Post.Edit = True
        Post.save()
    return redirect("index")

@login_required
def Profile(request):
    if request.POST.get("id") == None:
        USER = User.objects.get(username = request.user)
    else:
        USER = request.POST.get("id")   
        Follow_user = USER = User.objects.get(username = USER)

    posts = Posts.objects.all().filter(user = USER).order_by("id").reverse()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    fol_msg = ""
    if USER !=  User.objects.get(username = request.user):
        if len(Follower.objects.all().filter(User_followed = Follow_user).filter(followers =  User.objects.get(username = request.user))) == 0:
            fol_msg = "Follow user"
        else:
            fol_msg = "Unfollow user"

    Followers = []
    Following = []
    for Fol in Follower.objects.all().filter(User_followed = request.user):
        Followers.append(Fol.followers)

    for Fol in Follower.objects.all().filter(followers= request.user):
        Following.append(Fol.User_followed)

    return render(request, "network/index.html", {
        "fol_msg": fol_msg,
        "Followers": Followers,
        "Following": Following,
        "USER": USER,
        "Posts": page_obj,
    })

@login_required
def Follow(request):
    Follow_user = User.objects.get(username = request.POST.get("id"))
    Current_user = User.objects.get(username = request.user)
    
    if len(Follower.objects.all().filter(User_followed = Follow_user).filter(followers = Current_user)) == 0:
        fllw = Follower(
                User_followed = Follow_user,
                followers = Current_user
                )
        fllw.save()

        fol_msg = "Unfollow user"
        Error = "You followed " + str(Follow_user)
    else:
        fllw = Follower.objects.all().filter(User_followed = Follow_user).filter(followers = Current_user)
        fllw.delete()
        
        fol_msg = "Follow user"
        Error = "You unfollowed " + str(Follow_user)
        
    Followers = []
    Following = []
    for Fol in Follower.objects.all().filter(User_followed = request.user):
        Followers.append(Fol.followers)

    for Fol in Follower.objects.all().filter(followers= request.user):
        Following.append(Fol.User_followed)

    return render(request, "network/index.html", {
        "fol_msg": fol_msg,
        "Error": Error,
        "USER": Follow_user,
        "Posts": Posts.objects.all().filter(user = Follow_user),
        "Followers": Followers,
        "Following": Following,
    })


@login_required
def Show_Follow(request):
    user = Follower.objects.all().filter(followers = request.user)
    fol_posts = []
    all_posts = []
    if len(user) != 0:
        for i in user:
            fol_posts.append(Posts.objects.all().filter(user = i.User_followed))

        for k in range(len(fol_posts)):
            for j in fol_posts[k]:
                all_posts.append(j)

        paginator = Paginator(all_posts, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
        return render(request, "network/Follow.html", {
            "all_posts": all_posts,
            "Posts": page_obj,
            })
    else:
        Error ="You dont follow anyone."
        return render(request, "network/Follow.html", {
            "Error": Error
            })
# _______________________________________________________________________________________________

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
