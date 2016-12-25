import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from apps.users.models import EmailUser
from .models import Category, Subcategory, Thread, Post, Shout
from .forms import ThreadForm, PostForm, ShoutForm

def recent_threads():
    return Thread.objects.all().order_by('-created')[:5]

def recent_activity():
    return Thread.objects.all().order_by('-modified')[:5]

def get_subcategories(parent):
    return Subcategory.objects.filter(parent__id=parent.id).order_by('order')

def subcategory_threads(sub):
    return Thread.objects.filter(category__id=sub.id)

def subcategory_posts(sub):
    return Post.objects.filter(thread__category__id=sub.id)

def thread_posts(thread):
    return Post.objects.filter(thread__id=thread.id)

def index_view(request):
    category_groups = []
    parent_categories = Category.objects.all()
    for parent_category in parent_categories:
        children_groups = []
        children = Subcategory.objects.filter(parent__id=parent_category.id).order_by('order')
        for child in children:
            child_threads = Thread.objects.filter(category__id=child.id).order_by('-created')
            num_threads = len(child_threads)
            posts = Post.objects.filter(thread__category__id=child.id)
            num_posts = len(posts)
            children_groups.append({
                'category': child,
                'num_threads': num_threads,
                'num_posts': num_posts,
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
    return render(request, 'board/index.html', context)

def category_view(request, pk):
    category = Category.objects.get(id=pk)
    subcategories = []
    for sub in get_subcategories(category):
        num_threads = len(subcategory_threads(sub))
        num_posts = len(subcategory_posts(sub))
        subcategories.append({
            'obj': sub,
            'num_threads': num_threads,
            'num_posts': num_posts
        })
    context = {
        'category': category,
        'subcategories': subcategories
    }
    return render(request, 'board/category_view.html', context)

def subcategory_view(request, pk):
    category = Subcategory.objects.get(id=pk)
    threads = []
    for thread in subcategory_threads(category).order_by('-modified'):
        group = {
            'obj': thread,
            'num_posts': len(thread_posts(thread)),
        }
        threads.append(group)
    context = {
        'category': category,
        'threads': threads
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
        'posts': thread_posts(thread),
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
