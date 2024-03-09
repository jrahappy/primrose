from django.db import models
from django.urls import reverse
from django.conf import settings
from accounts.models import CustomUser


class Book(models.Model):
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    author = models.CharField(max_length=255, null=True, blank=True)
    cover = models.ImageField(upload_to="covers/", blank=True)
    description = models.TextField()
    product_name = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True
    )
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.CharField(max_length=100)
    sub_text = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    ordery = models.IntegerField(default=0)
    orderx = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("support:article-detail", kwargs={"pk": self.pk})
