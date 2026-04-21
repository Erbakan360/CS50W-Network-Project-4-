from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    content = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    Edit = models.BooleanField(default=False)
    like = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.content} @{self.time}. Likes: {self.like}"


class Like(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="liked_usr")
    liked_users = models.ManyToManyField(User, blank=True, related_name="liked_posts")


class Follower(models.Model):
    User_followed = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="follows")
    followers = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="followers")
