from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import EmailUser, Category, Subcategory, Thread, Post, Shout, \
Conversation, Message, Report
from .forms import ThreadForm, PostForm, ReportForm

def recent_threads():
    return Thread.objects.all().order_by('-created')

def recent_activity():
    return Thread.objects.all().order_by('-modified')

def index_view(request):
    category_groups = []
    parent_categories = Category.objects.all()
    if not request.user.is_authenticated:
        parent_categories = parent_categories.filter(
            auth_req=False).order_by('order')
    for parent_category in parent_categories:
        children_groups = []
        children = parent_category.subcategories
        if not request.user.is_authenticated:
            children = children.filter(auth_req=False).order_by('order')
        for child in children:
            children_groups.append({
                'category': child,
                'num_threads': len(child.threads),
                'num_posts': len(child.posts),
            })
        category_groups.append({
            'parent': parent_category,
            'children': children_groups
        })

    recent_thread_data = recent_threads()
    recent_activity_data = recent_activity()
    if not request.user.is_authenticated:
        recent_thread_data = recent_thread_data.filter(
            category__auth_req=False)
        recent_activity_data = recent_activity_data.filter(
            category__auth_req=False)

    newest_member = EmailUser.objects.all().order_by('-created').first()
    member_count = EmailUser.objects.all().count()
    context = {
        'categories': category_groups,
        'recent_threads': recent_thread_data[:5],
        'recent_activity': recent_activity_data[:5],
        'newest_member': newest_member,
        'member_count': member_count
    }
    return render(request, 'board/index.html', context)

def unpermitted_view(request):
    return render(request, 'board/unpermitted.html', {})

def my_profile(request):
    if not request.user.is_authenticated or request.user.is_banned:
        return redirect('board:unpermitted')
    context = {}
    return render(request, 'board/my_profile.html', context)

def settings_view(request):
    context = {}
    return render(request, 'board/settings.html', context)

def profile_view(request, username):
    user = EmailUser.objects.get(username=username)
    if not request.user.is_authenticated or request.user.is_banned:
        return redirect('board:unpermitted')
    if request.user.id == user.id:
        return redirect('board:me')
    context = {
        'profile': user
    }
    return render(request, 'board/profile_page.html', context)

def category_view(request, pk):
    category = Category.objects.get(id=pk)
    if not category.can_view(request.user):
        return unpermitted_view(request)
    subcategories = []
    for sub in category.subcategories:
        subcategories.append({
            'obj': sub,
            'can_post': sub.can_post(request.user),
            'num_threads': len(sub.threads),
            'num_posts': len(sub.posts)
        })
    context = {
        'category': category,
        'subcategories': subcategories
    }
    return render(request, 'board/category_view.html', context)

def subcategory_view(request, pk):
    category = Subcategory.objects.get(id=pk)
    if not category.can_view(request.user):
        return unpermitted_view(request)
    # Paginate threads
    paginator = Paginator(category.threads.order_by('-pinned', '-modified'), 20)
    page = request.GET.get('page')
    try:
        threads = paginator.page(page)
    except PageNotAnInteger:
        threads = paginator.page(1)
    except EmptyPage:
        threads = paginator.page(paginator.num_pages)
    context = {
        'can_post': category.can_post(request.user),
        'category': category,
        'threads': threads
    }
    return render(request, 'board/subcategory_view.html', context)

def thread_view(request, pk):
    thread = Thread.objects.get(id=pk)
    if not thread.can_view(request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return unpermitted_view(request)
        form = PostForm(request, request.POST)
        if form.is_valid():
            form.save(thread=thread, set_user=True)
            return redirect('board:thread', pk)
    else:
        form = PostForm(request)
    # Paginate posts
    paginator = Paginator(thread.posts.all(), 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'thread': thread,
        'posts': posts,
        'post_form': form,
    }
    return render(request, 'board/thread_view.html', context)

def thread_create(request, category_id):
    subcategory = Subcategory.objects.get(id=category_id)
    if not subcategory.can_post(request.user):
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
    if not instance.can_edit(request.user):
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
    if not instance.can_edit(request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        redirect_to = instance.category.id
        instance.delete()
        return redirect('board:subcategory', redirect_to)
    context = {
        'object': instance
    }
    return render(request, 'board/thread_delete_form.html', context)

def post_update(request, pk):
    instance = Post.objects.get(id=pk)
    if not instance.can_edit(request.user):
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
    if not instance.can_edit(request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        redirect_to = instance.thread.id
        instance.delete()
        return redirect('board:thread', redirect_to)
    context = {
        'object': instance
    }
    return render(request, 'board/post_delete_form.html', context)

def conversations_list(request):
    if request.user.is_authenticated and request.user.is_banned:
        return redirect('board:unpermitted')
    conversations = request.user.conversations.all()
    context = {
        'conversations': conversations
    }
    return render(request, 'board/conversations_list.html', context)

def reports_list(request):
    context = {
        'reports': Report.objects.all()
    }
    return render(request, 'board/reports_list.html', context)

def report_view(request, pk):
    instance = Report.objects.get(id=pk)
    if request.method == 'POST':
        instance.resolved = True
        instance.resolved_by = request.user
        instance.date_resolved = timezone.now()
        instance.save()
        return redirect('board:reports-list')
    context = {
        'report': Report.objects.get(id=pk)
    }
    return render(request, 'board/report_view.html', context)

def report_create(request, thread=None, post=None):
    if request.method == 'POST':
        form = ReportForm(request, request.POST)
        if form.is_valid():
            if thread:
                thread_obj = Thread.objects.get(id=thread)
                report = form.save(thread=thread_obj, set_user=True)
                return redirect('board:thread', thread)
            if post:
                post_obj = Post.objects.get(id=post)
                report = form.save(post=post_obj, set_user=True)
                return redirect('board:thread', post_obj.thread.id)
    else:
        form = ReportForm(request)
    context = {
        'form': form
    }
    return render(request, 'board/report_create_form.html', context)
