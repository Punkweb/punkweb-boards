import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from apps.users.models import EmailUser
from .models import Category, Subcategory, Thread, Post, Shout
from .forms import ThreadForm, PostForm, ShoutForm

def recent_threads():
    return Thread.objects.all().order_by('-created')

def recent_activity():
    return Thread.objects.all().order_by('-modified')

def get_subcategories(parent):
    return Subcategory.objects.filter(parent__id=parent.id).order_by('order')

def subcategory_threads(sub):
    return Thread.objects.filter(category__id=sub.id)

def subcategory_posts(sub):
    return Post.objects.filter(thread__category__id=sub.id)

def thread_posts(thread):
    return Post.objects.filter(thread__id=thread.id)

def can_post_in_sub(sub, user):
    if sub.admin_req and user.is_authenticated and user.is_admin:
        return True
    elif not sub.admin_req and user.is_authenticated:
        return True
    else:
        return False

def index_view(request):
    category_groups = []
    if request.user.id:
        parent_categories = Category.objects.all().order_by('order')
    else:
        parent_categories = Category.objects.filter(auth_req=False).order_by('order')
    for parent_category in parent_categories:
        children_groups = []
        if request.user.id:
            children = Subcategory.objects.filter(parent__id=parent_category.id).order_by('order')
        else:
            children = Subcategory.objects.filter(parent__id=parent_category.id, auth_req=False).order_by('order')
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
    if request.user.id is None:
        recent_thread_data = recent_threads().filter(category__auth_req=False)[:5]
        recent_activity_data = recent_activity().filter(category__auth_req=False)[:5]
    else:
        recent_thread_data = recent_threads()[:5]
        recent_activity_data = recent_activity()[:5]
    context = {
        'categories': category_groups,
        'recent_threads': recent_thread_data,
        'recent_activity': recent_activity_data
    }
    return render(request, 'board/index.html', context)

def unpermitted_view(request):
    return render(request, 'unpermitted.html', {})

def category_view(request, pk):
    category = Category.objects.get(id=pk)
    if category.auth_req and request.user.id is None:
        return unpermitted_view(request)
    subcategories = []
    for sub in get_subcategories(category):
        num_threads = len(subcategory_threads(sub))
        num_posts = len(subcategory_posts(sub))
        subcategories.append({
            'obj': sub,
            'can_post': can_post_in_sub(sub, request.user),
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
        'can_post': can_post_in_sub(category, request.user),
        'category': category,
        'threads': threads
    }
    return render(request, 'board/subcategory_view.html', context)

def thread_view(request, pk):
    thread = Thread.objects.get(id=pk)
    posts = Post.objects.filter(thread__id=thread.id)
    if thread.category.auth_req and request.user.id is None:
        return unpermitted_view(request)
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
            return redirect('board:shoutbox')
    else:
        shout_form = ShoutForm()
    context = {
        'shouts': shouts,
        'shout_form': shout_form
    }
    return render(request, 'board/shouts_view.html', context)


class ThreadCreate(CreateView):
    form_class = ThreadForm
    model = Thread
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        category = Subcategory.objects.get(id=self.kwargs['category_id'])
        thread = form.save(commit=False)
        thread.category = category
        thread.user = EmailUser.objects.get(id=self.request.user.id)
        thread.save()
        return super(ThreadCreate, self).form_valid(form)


class ThreadUpdate(UpdateView):
    form_class = ThreadForm
    model = Thread
    template_name_suffix = '_update_form'


class ThreadDelete(DeleteView):
    form_class = ThreadForm
    model = Thread
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('board:index')


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        thread = Thread.objects.get(id=self.kwargs['thread_id'])
        post = form.save(commit=False)
        post.thread = thread
        post.user = EmailUser.objects.get(id=self.request.user.id)
        post.save()
        return super(PostCreate, self).form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name_suffix = '_update_form'


class PostDelete(DeleteView):
    form_class = PostForm
    model = Post
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('board:index')


class ShoutCreate(CreateView):
    form_class = ShoutForm
    model = Shout
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        shout = form.save(commit=False)
        shout.user = EmailUser.objects.get(id=self.request.user.id)
        shout.save()
        return super(ShoutCreate, self).form_valid(form)


class ShoutUpdate(UpdateView):
    form_class = ShoutForm
    model = Shout
    template_name_suffix = '_update_form'


class ShoutDelete(DeleteView):
    form_class = ShoutForm
    model = Shout
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('board:index')
