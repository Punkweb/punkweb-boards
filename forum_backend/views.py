from django.shortcuts import render
from django.http import Http404
from apps.board.models import ParentCategory, ChildCategory, Post, Shout
from apps.board.forms import ShoutForm


def home_view(request):
    try:
        if request.method == 'POST':
            shout_form = ShoutForm(request.POST)
            if shout_form.is_valid():
                shout = shout_form.save(commit=False)
                shout.user = EmailUser.objects.get(id=request.user.id)
                shout.save()
        else:
            shout_form = ShoutForm()
        shouts = Shout.objects.all()[:10]
        category_groups = []
        parent_categories = ParentCategory.objects.all()
        for parent_category in parent_categories:
            children_groups = []
            children = ChildCategory.objects.filter(parent__id=parent_category.id).order_by('order')
            for child in children:
                child_posts = Post.objects.filter(category__id=child.id).order_by('created')
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
            'shout_form': shout_form,
            'shouts': shouts,
            'categories': category_groups
        }
    except:
        raise Http404('Error in home_view')
    return render(request, 'home.html', context)
