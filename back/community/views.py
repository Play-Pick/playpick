from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import (
    require_safe,
    require_POST,
    require_http_methods,
)
from .models import Article, Comment
from .forms import ArticleForm, CommentForm


@require_safe
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'community/index.html', context)

#@api_view([''])
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('community:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)


@require_safe
def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comments = article.comments.all()
    comment_form = CommentForm()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'community/detail.html', context)


@require_POST
def create_comment(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        return redirect('community:detail', article.pk)
    context = {
        'comment_form': comment_form,
        'article': article,
        'comments': article.comments.all(),
    }
    return render(request, 'community/detail.html', context)


@login_required
def like(request, article_pk):
    article = Article.objects.get(pk=article_pk)

    # 좋아요/좋아요 취소 토글
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        is_liked = False
    else:
        article.like_users.add(request.user)
        is_liked = True

    # AJAX 요청인지 확인
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.http import JsonResponse
        return JsonResponse({
            'is_liked': is_liked,
            'likes_count': article.like_users.count(),
        })

    return redirect('community:index')
