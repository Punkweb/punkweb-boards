from django.shortcuts import render
from django.http import Http404
from apps.board.models import Category, Subcategory, Post, Shout
from apps.board.forms import ShoutForm


def home_view(request):
    category_groups = []
    parent_categories = Category.objects.all()
    for parent_category in parent_categories:
        children_groups = []
        children = Subcategory.objects.filter(parent__id=parent_category.id).order_by('order')
        for child in children:
            child_posts = Post.objects.filter(category__id=child.id).order_by('-created')
            last_post = child_posts.first()
            children_groups.append({
                'category': child,
                'num_posts': len(child_posts),
                'last_post': last_post
            })
        category_groups.append({
            'parent': parent_category,
            'children': children_groups
        })
    context = {
        'categories': category_groups
    }
    return render(request, 'home.html', context)
