from django.http import Http404
from django.shortcuts import render
from .models import ParentCategory, ChildCategory, Post, Shout


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


def shouts_view(request):
    try:
        shouts = Shout.objects.all()
        context = {
            'shouts': shouts,
        }
    except:
        raise Http404('Error in shouts_view')
    return render(request, 'board/shouts_view.html', context)
