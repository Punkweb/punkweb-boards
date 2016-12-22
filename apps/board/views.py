import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from apps.users.models import EmailUser
from .models import Category, Subcategory, Thread, Post, Shout
from .forms import ThreadForm, PostForm, ShoutForm


def category_view(request, pk):
    category = Category.objects.get(id=pk)
    sub_groups = []
    subcategories = Subcategory.objects.filter(parent__id=category.id).order_by('order')
    for sub in subcategories:
        threads = Thread.objects.filter(category__id=sub.id)
        num_threads = len(threads)
        posts = Post.objects.filter(thread__category__id=sub.id)
        num_posts = len(posts)
        sub_groups.append({
            'category': sub,
            'num_threads': num_threads,
            'num_posts': num_posts
        })
    context = {
        'category': category,
        'subcategories': sub_groups
    }
    return render(request, 'board/category_view.html', context)


def subcategory_view(request, pk):
    category = Subcategory.objects.get(id=pk)
    thread_groups = []
    threads = Thread.objects.filter(category__id=pk).order_by('-modified')
    for thread in threads:
        posts = Post.objects.filter(thread_id=thread.id)
        group = {
            'thread': thread,
            'num_posts': len(posts),
        }
        thread_groups.append(group)
    context = {
        'category': category,
        'threads': thread_groups
    }
    return render(request, 'board/subcategory_view.html', context)

def thread_view(request, pk):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = Thread.objects.get(id=pk)
            post.thread.modified = datetime.datetime.now()
            post.thread.save()
            post.user = EmailUser.objects.get(id=request.user.id)
            post.save()
            return redirect('board:thread', pk)
    else:
        form = PostForm()
    thread = Thread.objects.get(id=pk)
    posts = Post.objects.filter(thread__id=thread.id)
    context = {
        'thread': thread,
        'posts': posts,
        'post_form': form,
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


class PostCreate(CreateView):
    model = Post
    fields = ['content']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        thread = Thread.objects.get(id=self.kwargs['thread_id'])
        post = form.save(commit=False)
        post.thread = thread
        post.user = EmailUser.objects.get(id=self.request.user.id)
        post.save()
        return super(PostCreate, self).form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    fields = ['content']
    template_name_suffix = '_update_form'


class PostDelete(DeleteView):
    model = Post
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('home')


class ShoutCreate(CreateView):
    model = Shout
    fields = ['content']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        shout = form.save(commit=False)
        shout.user = EmailUser.objects.get(id=self.request.user.id)
        shout.save()
        return super(ShoutCreate, self).form_valid(form)


class ShoutUpdate(UpdateView):
    model = Shout
    fields = ['content']
    template_name_suffix = '_update_form'


class ShoutDelete(DeleteView):
    model = Shout
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('home')
