from django.shortcuts import render
from django.http import Http404
from apps.board.models import Category, Subcategory, Thread, Comment, Shout
from apps.board.forms import ShoutForm


def home_view(request):
    category_groups = []
    parent_categories = Category.objects.all()
    for parent_category in parent_categories:
        children_groups = []
        children = Subcategory.objects.filter(parent__id=parent_category.id).order_by('order')
        for child in children:
            child_threads = Thread.objects.filter(category__id=child.id).order_by('-created')
            num_threads = len(child_threads)
            comments = Comment.objects.filter(thread__category__id=child.id)
            num_comments = len(comments)
            children_groups.append({
                'category': child,
                'num_threads': num_threads,
                'num_comments': num_comments,
            })
        category_groups.append({
            'parent': parent_category,
            'children': children_groups
        })
    recent_threads = Thread.objects.all().order_by('-created')[:5]
    recent_activity = Thread.objects.all().order_by('-modified')[:5]
    context = {
        'categories': category_groups,
        'recent_threads': recent_threads,
        'recent_activity': recent_activity
    }
    return render(request, 'home.html', context)
