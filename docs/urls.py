from django.urls import path
from . import views

app_name = "docs"
urlpatterns = [
    # path("", views.article_list, name="article-list"),
    # path("create/", views.article_create, name="article-create"),
    # path("<int:pk>", views.article_detail, name="article-detail"),
    # path("<int:pk>/update", views.article_update, name="article-update"),
    # path("<int:pk>/delete", views.article_delete, name="article-delete"),
    path("", views.book_list, name="book-list"),
    path("layout/", views.layout, name="layout"),
    path("book/create/", views.book_create, name="book-create"),
    path("book/<int:pk>/", views.book_detail, name="book-detail"),
    path("book/<int:pk>/update", views.book_update, name="book-edit"),
    path("book/<int:pk>/delete", views.book_delete, name="book-delete"),
    path("article/", views.book_delete, name="article-list"),
    path("article/create/", views.article_create, name="article-create"),
    path("article/<int:pk>/", views.article_detail, name="article-detail"),
    path("article/<int:pk>/update", views.article_update, name="article-edit"),
    path("article/<int:pk>/delete", views.article_delete, name="article-delete"),
]
