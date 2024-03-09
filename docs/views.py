from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Book as book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ArticleForm
from django.utils import timezone


def layout(request):
    return render(request, "docs/layout.html")


def book_list(request):
    books = Book.objects.all()
    paginator = Paginator(books, 10)
    page = request.GET.get("page")
    books = paginator.get_page(page)
    page_obj = paginator.get_page(page)
    context = {
        "app_name": app_name,
        "nav_list": nav_list,
        "side_list": side_list,
        "breadcrumb": breadcrumb,
        "title": title,
        "books": books,
        "model1_list": model1_list,
        "model2_list": model2_list,
    }
    return render(request, "docs/book_list.html", context)


def book_detail(request, pk):
    book = Book.objects.get_object_or_404(pk=pk)
    model1_list = model1.objects.all()
    context = {
        "app_name": app_name,
        "nav_list": nav_list,
        "side_list": side_list,
        "breadcrumb": breadcrumb,
        "title": title,
        "books": books,
        "model1_list": model1_list,
        "user": request.user,
    }
    return render(request, "docs/book_detail.html", context)


def book_create(request):
    context = {
        "app_name": app_name,
        "nav_list": nav_list,
        "side_list": side_list,
        "breadcrumb": breadcrumb,
        "title": title,
        "model1_list": model1_list,
        "user": request.user,
    }
    if request.method == "POST":
        form = bookForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            user = request.user
            form.save()
            return redirect("docs:book-list")
    else:
        form = bookForm()
    context["form"] = form
    return render(request, "docs/book_create.html", {"form": form})


def book_update(request, pk):
    context = {
        "app_name": app_name,
        "nav_list": nav_list,
        "side_list": side_list,
        "breadcrumb": breadcrumb,
        "title": title,
        "model1_list": model1_list,
        "user": request.user,
    }
    if request.method == "POST":
        book = Book.objects.get_object_or_404(pk=pk)
        form = bookForm(request.POST, instance=book)
        if form.is_valid():
            form = form.save(commit=False)
            updated_at = timezone.now()
            form.save()
            return redirect("docs:book-list")
    else:
        book = Book.get_object_or_404(pk=pk)
        form = bookForm(instance=book)
    context["form"] = form
    return render(request, "docs/book_edit.html", context)


def book_delete(request, pk):
    book = Book.objects.get_object_or_404(pk=pk)
    book.delete()
    return redirect("docs:book-list")


def article_list(request):
    articles = Article.objects.all().order_by("-created_at")
    paginator = Paginator(articles, 10)
    page = request.GET.get("page")
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, "docs/article_list.html", {"page_obj": articles})


def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    return render(request, "docs/article_detail.html", {"article": article})


def article_create(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            user = request.user
            form.save()
            return redirect("docs:article-list")
    else:
        form = ArticleForm()
    return render(request, "docs/article_create.html", {"form": form})


def article_update(request, pk):
    article = Article.objects.get(pk=pk)
    form = ArticleForm(instance=article)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form = form.save(commit=False)
            user = request.user
            form.save()
            return redirect("docs:article-list")
    else:
        form = ArticleForm(instance=article)
        article_id = article.id

    return render(
        request, "docs/article_update.html", {"form": form, "article_id": article_id}
    )


def article_delete(request, pk):
    doc = Article.objects.get(pk=pk)
    doc.delete()
    return redirect("docs:article-list")
