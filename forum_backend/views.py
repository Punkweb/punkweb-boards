from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from apps.users.models import EmailUser
from apps.board.models import ParentCategory, ChildCategory, Post, Comment, Shout


class HomePage(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        shouts = Shout.objects.all()
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
            'shouts': shouts,
            'categories': category_groups
        }
        return self.render_to_response(context)
