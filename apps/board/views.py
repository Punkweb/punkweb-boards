from django.http import Http404
from django.shortcuts import render, redirect
from apps.users.models import EmailUser
from .models import ParentCategory, ChildCategory, Post, Shout
from .forms import PostForm, ShoutForm


def category_view(request, category_id):
    try:
        parent = ParentCategory.objects.get(id=category_id)
        children_groups = []
        children = ChildCategory.objects.filter(parent__id=parent.id).order_by('order')
        for child in children:
            child_posts = Post.objects.filter(category__id=child.id).order_by('created')
            last_post = child_posts.first()
            children_groups.append({
                'category': child,
                'num_posts': len(child_posts),
                'last_post': last_post
            })
        context = {
            'parent': parent,
            'children': children_groups
        }
    except:
        raise Http404('Category does not exist')
    return render(request, 'board/category_view.html', context)


def topic_view(request, category_id):
    try:
        category = ChildCategory.objects.get(id=category_id)
        posts = Post.objects.filter(category__id=category_id)
        context = {
            'category': category,
            'posts': posts
        }
    except:
        raise Http404('Post does not exist')
    return render(request, 'board/topic_view.html', context)


def post_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        context = {
            'post': post
        }
    except:
        raise Http404('Post does not exist')
    return render(request, 'board/post_view.html', context)


def new_post(request, category_id):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = EmailUser.objects.get(id=request.user.id)
            post.category = ChildCategory.objects.get(id=category_id)
            post.save()
            return redirect('home')
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
