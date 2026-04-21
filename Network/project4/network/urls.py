
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("New_Post", views.New_Post, name="New_Post"),
    path("Save_Edit", views.Save_Edit, name="Save_Edit"),
    path("Edit", views.Edit, name="Edit"),
    path("Likes", views.Likes, name="Likes"),
    path("Follow", views.Follow, name="Follow"),
    path("Profile", views.Profile, name="Profile"),
    path("Show_Follow", views.Show_Follow, name="Show_Follow"),
]
