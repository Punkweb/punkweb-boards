import datetime
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from apps.common.base import QueryView
from apps.users.models import EmailUser
from .models import Category, Subcategory, Post, Comment, Shout
from .forms import PostForm, CommentForm, ShoutForm
from . import queries


class CategoryView(QueryView):
    template_name = 'board/category_view.html'

    def get_queries(self):
        return [queries.CategoryQuery(self.kwargs['category_id'])]


class SubCategoryView(QueryView):
    template_name = 'board/topic_view.html'

    def get_queries(self):
        return [queries.SubCategoryQuery(self.kwargs['category_id'])]


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
