import datetime
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from apps.users.models import EmailUser
from .models import Category, Subcategory, Post, Comment, Shout
from .forms import PostForm, CommentForm, ShoutForm


def category_view(request, pk):
    category = Category.objects.get(id=pk)
    sub_groups = []
    subcategories = Subcategory.objects.filter(parent__id=category.id).order_by('order')
    for sub in subcategories:
        posts = Post.objects.filter(category__id=sub.id).order_by('-created')
        num_posts = len(posts)
        comments = Comment.objects.filter(post__category__id=sub.id)
        num_comments = len(comments)
        sub_groups.append({
            'category': sub,
            'num_posts': num_posts,
            'num_comments': num_comments
        })
    context = {
        'category': category,
        'subcategories': sub_groups
    }
    return render(request, 'board/category_view.html', context)


def subcategory_view(request, pk):
    category = Subcategory.objects.get(id=pk)
    post_groups = []
    posts = Post.objects.filter(category__id=pk).order_by('-created')
    for post in posts:
        comments = Comment.objects.filter(post_id=post.id).order_by('-created')
        group = {
            'post': post,
            'num_comments': len(comments),
        }
        post_groups.append(group)
    context = {
        'category': category,
        'posts': post_groups
    }
    return render(request, 'board/subcategory_view.html', context)

def post_view(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(id=pk)
            comment.post.modified = datetime.datetime.now()
            comment.post.save()
            comment.user = EmailUser.objects.get(id=request.user.id)
            comment.save()
            return redirect('board:post', pk)
    else:
        form = CommentForm()
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post__id=post.id)
    context = {
        'post': post,
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'board/post_view.html', context)


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


class CategoryCreate(CreateView):
    model = Category
    fields = ['name', 'description', 'order']
    template_name_suffix = '_create_form'


class CategoryUpdate(UpdateView):
    model = Category
    fields = ['name', 'description', 'order']
    template_name_suffix = '_update_form'


class CategoryDelete(DeleteView):
    model = Category
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('home')


class SubcategoryCreate(CreateView):
    model = Subcategory
    fields = ['name', 'description', 'order']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        category = Category.objects.get(id=self.kwargs['category_id'])
        sub = form.save(commit=False)
        sub.parent = category
        sub.save()
        return super(SubcategoryCreate, self).form_valid(form)


class SubcategoryUpdate(UpdateView):
    model = Subcategory
    fields = ['name', 'description', 'order']
    template_name_suffix = '_update_form'


class SubcategoryDelete(DeleteView):
    model = Subcategory
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('home')


class PostCreate(CreateView):
    model = Post
    fields = ['title', 'content']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        category = Subcategory.objects.get(id=self.kwargs['category_id'])
        post = form.save(commit=False)
        post.category = category
        post.user = EmailUser.objects.get(id=self.request.user.id)
        post.save()
        return super(PostCreate, self).form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name_suffix = '_update_form'


class PostDelete(DeleteView):
    model = Post
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('home')


class CommentCreate(CreateView):
    model = Comment
    fields = ['content']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        post = Post.objects.get(id=self.kwargs['post_id'])
        comment = form.save(commit=False)
        comment.post = post
        comment.user = EmailUser.objects.get(id=self.request.user.id)
        comment.save()
        return super(CommentCreate, self).form_valid(form)


class CommentUpdate(UpdateView):
    model = Comment
    fields = ['content']
    template_name_suffix = '_update_form'


class CommentDelete(DeleteView):
    model = Comment
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('home')


class ShoutCreate(CreateView):
    model = Shout
    fields = ['content']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = EmailUser.objects.get(id=self.request.user.id)
        comment.save()
        return super(ShoutCreate, self).form_valid(form)


class ShoutUpdate(UpdateView):
    model = Shout
    fields = ['content']
    template_name_suffix = '_update_form'


class ShoutDelete(DeleteView):
    model = Shout
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('home')
