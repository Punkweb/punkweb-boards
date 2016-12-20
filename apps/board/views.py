import datetime
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from apps.users.models import EmailUser
from .models import Category, Subcategory, Thread, Comment, Shout
from .forms import ThreadForm, CommentForm, ShoutForm


def category_view(request, pk):
    category = Category.objects.get(id=pk)
    sub_groups = []
    subcategories = Subcategory.objects.filter(parent__id=category.id).order_by('order')
    for sub in subcategories:
        threads = Thread.objects.filter(category__id=sub.id).order_by('-created')
        num_threads = len(threads)
        comments = Comment.objects.filter(thread__category__id=sub.id)
        num_comments = len(comments)
        sub_groups.append({
            'category': sub,
            'num_threads': num_threads,
            'num_comments': num_comments
        })
    context = {
        'category': category,
        'subcategories': sub_groups
    }
    return render(request, 'board/category_view.html', context)


def subcategory_view(request, pk):
    category = Subcategory.objects.get(id=pk)
    thread_groups = []
    threads = Thread.objects.filter(category__id=pk).order_by('-created')
    for thread in threads:
        comments = Comment.objects.filter(thread_id=thread.id).order_by('-created')
        group = {
            'thread': thread,
            'num_comments': len(comments),
        }
        thread_groups.append(group)
    context = {
        'category': category,
        'threads': thread_groups
    }
    return render(request, 'board/subcategory_view.html', context)

def thread_view(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = Thread.objects.get(id=pk)
            comment.thread.modified = datetime.datetime.now()
            comment.thread.save()
            comment.user = EmailUser.objects.get(id=request.user.id)
            comment.save()
            return redirect('board:thread', pk)
    else:
        form = CommentForm()
    thread = Thread.objects.get(id=pk)
    comments = Comment.objects.filter(thread__id=thread.id)
    context = {
        'thread': thread,
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'board/thread_view.html', context)


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


class ThreadCreate(CreateView):
    model = Thread
    fields = ['title', 'content']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        category = Subcategory.objects.get(id=self.kwargs['category_id'])
        thread = form.save(commit=False)
        thread.category = category
        thread.user = EmailUser.objects.get(id=self.request.user.id)
        thread.save()
        return super(ThreadCreate, self).form_valid(form)


class ThreadUpdate(UpdateView):
    model = Thread
    fields = ['title', 'content']
    template_name_suffix = '_update_form'


class ThreadDelete(DeleteView):
    model = Thread
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('home')


class CommentCreate(CreateView):
    model = Comment
    fields = ['content']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        thread = Thread.objects.get(id=self.kwargs['thread_id'])
        comment = form.save(commit=False)
        comment.thread = thread
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
