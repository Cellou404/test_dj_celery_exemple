import uuid
from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, verbose_name="title")
    content = models.TextField(verbose_name="content")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        verbose_name="author",
        related_name="articles")
    is_top_article = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    content = models.TextField(verbose_name="content")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        verbose_name="author",
        related_name="comments")
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, 
        verbose_name="article",
        related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.author.username} - {self.updated_at}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.email
