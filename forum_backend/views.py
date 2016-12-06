from django.views.generic import TemplateView
from django.shortcuts import redirect
from apps.users.models import EmailUser
from apps.board.models import ParentCategory, ChildCategory, Post, Comment


class HomePage(TemplateView):
    template_name = 'pages/home.html'

    def get(self, request, *args, **kwargs):
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
            'categories': category_groups
        }
        return self.render_to_response(context)


class ParentCategoryPage(TemplateView):
    template_name = 'pages/parent_category.html'

    def get(self, request, *args, **kwargs):
        category = ParentCategory.objects.get(id=self.kwargs.get('uuid'))
        children = ChildCategory.objects.filter(parent__id=category.id)

        context = {
            'parent': category,
            'children': children
        }
        return self.render_to_response(context)


class ChildCategoryPage(TemplateView):
    template_name = 'pages/child_category.html'

    def get(self, request, *args, **kwargs):
        category = ChildCategory.objects.get(id=self.kwargs.get('uuid'))
        posts = Post.objects.filter(category__id=category.id).order_by('created')

        context = {
            'category': category,
            'posts': posts
        }
        return self.render_to_response(context)


class PostPage(TemplateView):
    template_name = 'pages/post.html'

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs.get('uuid'))

        comments = Comment.objects.filter(post__id=post.id)

        context = {
            'post': post,
            'comments': comments
        }
        return self.render_to_response(context)


class MyProfilePage(TemplateView):
    template_name = 'pages/my_profile.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user

        context = {
            'user': user
        }
        return self.render_to_response(context)


class ProfileSettingsPage(TemplateView):
    template_name = 'pages/profile_settings.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user

        context = {
            'user': user
        }
        return self.render_to_response(context)


class ProfilePage(TemplateView):
    template_name = 'pages/profile.html'

    def get(self, request, *args, **kwargs):
        user = EmailUser.objects.get(id=self.kwargs.get('uuid'))

        if user != self.request.user:
            print('here')
            return redirect('me')

        context = {
            'user': user
        }
        return self.render_to_response(context)
