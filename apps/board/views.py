from django.shortcuts import render, redirect
from .models import Category, Subcategory, Thread, Post
from .forms import ThreadForm, PostForm

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
    return Post.objects.filter(thread__id=thread.id).order_by('created')

def can_post_in_sub(sub, user):
    if sub.admin_req and user.is_authenticated and user.is_admin:
        return True
    elif not sub.admin_req and user.is_authenticated:
        return True
    else:
        return False

def can_edit_post(instance, user):
    if user.is_authenticated and user.is_admin:
        return True
    elif instance.user.id == user.id:
        return True
    else:
        return False

def can_view_thread(instance, user):
    if instance.category.auth_req and not user.is_authenticated:
        return False
    else:
        return True

def can_view_category(instance, user):
    if instance.auth_req and not user.is_authenticated:
        return False
    else:
        return True

def index_view(request):
    category_groups = []
    if request.user.is_authenticated:
        parent_categories = Category.objects.all().order_by('order')
    else:
        parent_categories = Category.objects.filter(
            auth_req=False).order_by('order')
    for parent_category in parent_categories:
        children_groups = []
        if request.user.is_authenticated:
            children = Subcategory.objects.filter(
                parent__id=parent_category.id).order_by('order')
        else:
            children = Subcategory.objects.filter(
                parent__id=parent_category.id, auth_req=False
            ).order_by('order')
        for child in children:
            child_threads = Thread.objects.filter(
                category__id=child.id).order_by('-created')
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
    if not request.user.is_authenticated:
        recent_thread_data = recent_threads().filter(
            category__auth_req=False)[:5]
        recent_activity_data = recent_activity().filter(
            category__auth_req=False)[:5]
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
    if not can_view_category(category, request.user):
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
    if not can_view_category(category, request.user):
        return unpermitted_view(request)
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
    if not can_view_thread(thread, request.user):
        return unpermitted_view(request)
    if thread.category.auth_req and request.user.id is None:
        return unpermitted_view(request)
    if request.method == 'POST':
        if request.user.id is None:
            return unpermitted_view(request)
        form = PostForm(request, request.POST)
        if form.is_valid():
            form.save(thread=thread, set_user=True)
            return redirect('board:thread', pk)
    else:
        form = PostForm(request)
    context = {
        'thread': thread,
        'posts': thread_posts(thread),
        'post_form': form,
    }
    return render(request, 'board/thread_view.html', context)

def thread_create(request, category_id):
    subcategory = Subcategory.objects.get(id=category_id)
    if not can_post_in_sub(subcategory, request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        form = ThreadForm(request, request.POST)
        if form.is_valid():
            thread = form.save(category=subcategory, set_user=True)
            return redirect('board:thread', thread.id)
    else:
        form = ThreadForm(request)
    context = {
        'form': form
    }
    return render(request, 'board/thread_create_form.html', context)

def thread_update(request, pk):
    instance = Thread.objects.get(id=pk)
    if not can_edit_post(instance, request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        form = ThreadForm(request, request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('board:thread', pk)
    else:
        form = ThreadForm(request, instance=instance)
    context = {
        'form': form
    }
    return render(request, 'board/thread_update_form.html', context)

def thread_delete(request, pk):
    instance = Thread.objects.get(id=pk)
    if not can_edit_post(instance, request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        redirect_to = instance.category.id
        instance.delete()
        return redirect('board:subcategory', redirect_to)
    context = {}
    return render(request, 'board/thread_delete_form.html', context)

def post_update(request, pk):
    instance = Post.objects.get(id=pk)
    if not can_edit_post(instance, request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        form = PostForm(request, request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('board:thread', instance.thread.id)
    else:
        form = PostForm(request, instance=instance)
    context = {
        'form': form
    }
    return render(request, 'board/post_update_form.html', context)

def post_delete(request, pk):
    instance = Post.objects.get(id=pk)
    if not can_edit_post(instance, request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        redirect_to = instance.thread.id
        instance.delete()
        return redirect('board:thread', redirect_to)
    context = {}
    return render(request, 'board/thread_delete_form.html', context)
