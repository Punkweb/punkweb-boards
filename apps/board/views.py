from django.http import Http404
from django.shortcuts import render, redirect
from apps.users.models import EmailUser
from .models import Category, Subcategory, Post, Comment, Shout
from .forms import PostForm, CommentForm, ShoutForm
from . import queries


def category_view(request, category_id):
    query = queries.CategoryQuery(category_id)
    return render(request, 'board/category_view.html', query.get_context())


def topic_view(request, category_id):
    query = queries.SubCategoryQuery(category_id)
    return render(request, 'board/topic_view.html', query.get_context())


def post_view(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(id=post_id)
            comment.user = EmailUser.objects.get(id=request.user.id)
            comment.save()
            return redirect('board:post', post_id)
    else:
        form = CommentForm()
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post_id=post.id)
    context = {
        'post': post,
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'board/post_view.html', context)


def new_post(request, category_id):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = EmailUser.objects.get(id=request.user.id)
            post.category = Subcategory.objects.get(id=category_id)
            post.save()
            return redirect('board:post', post.id)
    else:
        form = PostForm()
    return render(request, 'board/new_post.html', {'form': form})


def shouts_view(request):
    shouts = Shout.objects.all()[:30]
    if request.method == 'POST':
        shout_form = ShoutForm(request.POST)
        if shout_form.is_valid():
            shout = shout_form.save(commit=False)
            shout.user = EmailUser.objects.get(id=request.user.id)
            shout.save()
    else:
        shout_form = ShoutForm()
    context = {
        'shouts': shouts,
        'shout_form': shout_form
    }
    return render(request, 'board/shouts_view.html', context)
