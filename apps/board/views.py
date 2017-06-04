from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, reverse
from django.utils import timezone

from .settings import BOARD_THEME
from apps.api.models import (
    EmailUser, Category, Subcategory, Thread, Post, Report, Conversation,
    Message, Notification, Shout
)
from .forms import (
    ThreadForm, PostForm, ReportForm, MessageForm, RegistrationForm,
    SettingsForm, KeywordSearchForm
)


def base_context(request):
    ctx = {}
    if request.user.is_authenticated and not request.user.is_banned:
        ctx.update({
            'unread_conversations': request.user.unread_conversations.count()
        })
        ctx.update({
            'unread_notifications': request.user.notifications.filter(read=False).count()
        })
        if request.user.is_staff:
            unresolved_reports = Report.objects.filter(resolved=False).count()
            ctx.update({'unresolved_reports': unresolved_reports})
    return ctx


def unpermitted_view(request):
    return render(
        request, 'board/themes/{}/unpermitted.html'.format(BOARD_THEME), {})


def index_view(request):
    total_posts = Post.objects.all().count()
    total_threads = Thread.objects.all().count()
    last_25_shouts = Shout.objects.all().select_related()[:25]

    category_groups = []
    parent_categories = Category.objects.all().order_by('order')
    if not request.user.is_authenticated:
        parent_categories = parent_categories.filter(auth_req=False)
    for parent_category in parent_categories:
        children = parent_category.subcategories
        if not request.user.is_authenticated:
            # Filter out categories with auth_req = True
            children = children.filter(
                auth_req=False, parent__auth_req=False).order_by('order')
        category_groups.append({
            'parent': parent_category,
            'children': children
        })
    recent_threads = Thread.objects.all().order_by('-created')
    recent_activity = Thread.objects.all().order_by('-modified')
    if not request.user.is_authenticated:
        # Filter out activity in subcategories with auth_req = True
        recent_threads = recent_threads.filter(
            category__auth_req=False, category__parent__auth_req=False)
        recent_activity = recent_activity.filter(
            category__auth_req=False, category__parent__auth_req=False)
    newest_member = EmailUser.objects.all().order_by('-created').first()
    member_count = EmailUser.objects.all().count()
    context = {
        'total_posts': total_posts,
        'total_threads': total_threads,
        'shouts': last_25_shouts,
        'categories': category_groups,
        'recent_threads': recent_threads[:5],
        'recent_activity': recent_activity[:5],
        'newest_member': newest_member,
        'member_count': member_count
    }
    context.update(base_context(request))
    return render(
        request, 'board/themes/{}/index.html'.format(BOARD_THEME), context)


def keyword_search_view(request):
    if not request.user.is_authenticated or request.user.is_banned:
        return redirect('board:unpermitted')

    if request.GET.get('keyword'):
        keyword = request.GET['keyword']
    else:
        keyword = ''

    user_vector = TrigramSimilarity(
        'username', keyword
    ) + TrigramSimilarity(
        'email', keyword
    )
    thread_vector = TrigramSimilarity(
        'title', keyword
    ) + TrigramSimilarity(
        'content', keyword
    ) + TrigramSimilarity(
        'user__username', keyword
    )
    post_vector = TrigramSimilarity(
        'content', keyword
    )
    matched_users = EmailUser.objects.annotate(
        similarity=user_vector,
    ).filter(similarity__gt=0.3).order_by('-similarity')
    matched_threads = Thread.objects.annotate(
        similarity=thread_vector,
    ).filter(similarity__gt=0.3).order_by('-similarity')
    matched_threads = Thread.objects.annotate(
        similarity=thread_vector,
    ).filter(similarity__gt=0.3).order_by('-similarity')
    matched_posts = Post.objects.annotate(
        similarity=post_vector,
    ).filter(similarity__gt=0.3).order_by('-similarity')
    context = {
        'matched_users': matched_users,
        'matched_threads': matched_threads,
        'matched_posts': matched_posts,
        'keyword': keyword
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/keyword_search.html'.format(BOARD_THEME),
        context
    )


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = EmailUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            return redirect('/board/login/')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    context.update(base_context(request))
    return render(
        request, 'board/themes/{}/register.html'.format(BOARD_THEME), context)


def my_profile(request):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.is_banned:
        return unpermitted_view(request)
    context = {}
    context.update(base_context(request))
    return render(
        request, 'board/themes/{}/my_profile.html'.format(BOARD_THEME), context)


def settings_view(request):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.is_banned:
        return unpermitted_view(request)
    if request.method == 'POST':
        form = SettingsForm(request, request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['image']:
                request.user.image = form.cleaned_data['image']
            if form.cleaned_data['gender']:
                request.user.gender = form.cleaned_data['gender']
            if form.cleaned_data['birthday']:
                request.user.birthday = form.cleaned_data['birthday']
            if form.cleaned_data['signature']:
                request.user.signature = form.cleaned_data['signature']
            request.user.save()
            return redirect('/board/me/')
    else:
        form = SettingsForm(request)
    context = {
        'form': form
    }
    context.update(base_context(request))
    return render(
        request, 'board/themes/{}/settings.html'.format(BOARD_THEME), context)


def profile_view(request, username):
    user = EmailUser.objects.get(username=username)
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.is_banned:
        return unpermitted_view(request)
    # Redirect to /board/me/ if trying to view own profile.
    if request.user.id == user.id:
        # TODO do not redirect so that users
        # can view their profile as others see it.
        return my_profile(request)
    context = {
        'profile': user
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/profile_page.html'.format(BOARD_THEME),
        context
    )


def category_view(request, pk):
    category = Category.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have view
    # permissions on this category.
    if not category.can_view(request.user):
        return unpermitted_view(request)
    subcategories = []

    subs = category.subcategories.order_by('order')
    if not request.user.is_authenticated:
        subs = subs.filter(
            auth_req=False, parent__auth_req=False)
    for sub in category.subcategories:
        if sub.can_view(request.user):
            subcategories.append({
                'obj': sub,
                'can_post': sub.can_post(request.user),
            })
    context = {
        'category': category,
        'subcategories': subcategories
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/category_view.html'.format(BOARD_THEME),
        context
    )


def subcategory_view(request, pk):
    category = Subcategory.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have view
    # permissions on this subcategory.
    if not category.can_view(request.user):
        return unpermitted_view(request)
    # Paginate threads
    # TODO: get correct ordering worked out
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
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/subcategory_view.html'.format(BOARD_THEME),
        context
    )


def thread_view(request, pk):
    thread = Thread.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have view
    # permissions on this thread.
    if not thread.can_view(request.user):
        return unpermitted_view(request)
    # Paginate posts
    paginator = Paginator(thread.posts.order_by('created'), 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # Logic for creating a new post on a thread
    if request.method == 'POST':
        # Redirect to unpermitted page if not logged in.
        if not request.user.is_authenticated or thread.closed:
            return unpermitted_view(request)
        form = PostForm(request, request.POST)
        if form.is_valid():
            form.save(thread=thread, set_user=True)
            # Redirect to the last page of posts,
            # which is where this new post will be.
            return redirect('/board/thread/{}/?page={}'.format(
                thread.id, paginator.num_pages))
    else:
        form = PostForm(request)
    context = {
        'thread': thread,
        'posts': posts,
        'post_form': form,
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/thread_view.html'.format(BOARD_THEME),
        context
    )


def thread_create(request, category_id):
    subcategory = Subcategory.objects.get(id=category_id)
    # Redirect to unpermitted page if the requesting user does not have post
    # permission in this category.
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
        'form': form,
        'subcategory': subcategory
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/thread_create_form.html'.format(BOARD_THEME),
        context
    )


def thread_update(request, pk):
    instance = Thread.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have edit
    # permissions on this thread.
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
        'form': form,
        'object': instance
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/thread_update_form.html'.format(BOARD_THEME),
        context
    )


def thread_delete(request, pk):
    instance = Thread.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have edit
    # permissions on this thread.
    if not instance.can_edit(request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        redirect_to = instance.category.id
        instance.delete()
        return redirect('board:subcategory', redirect_to)
    context = {
        'object': instance
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/thread_delete_form.html'.format(BOARD_THEME),
        context
    )


# There is no post_view or post_create as both are handled on the thread_view

def post_update(request, pk):
    instance = Post.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have edit
    # permissions on this post.
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
        'form': form,
        'obj': instance
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/post_update_form.html'.format(BOARD_THEME),
        context
    )


def post_delete(request, pk):
    instance = Post.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have edit
    # permissions on this post.
    if not instance.can_edit(request.user):
        return unpermitted_view(request)
    if request.method == 'POST':
        redirect_to = instance.thread.id
        instance.delete()
        return redirect('board:thread', redirect_to)
    context = {
        'object': instance
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/post_delete_form.html'.format(BOARD_THEME),
        context
    )


def conversations_list(request):
    # Redirect to unpermitted page if not authenticated or is banned
    if not request.user.is_authenticated or request.user.is_banned:
        return unpermitted_view(request)
    conversations = request.user.conversations.all()
    context = {
        'conversations': conversations
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/inbox.html'.format(BOARD_THEME),
        context
    )


def conversation_view(request, pk):
    # Redirect to unpermitted page if not authenticated or is banned
    if not request.user.is_authenticated or request.user.is_banned:
        return unpermitted_view(request)
    conversation = request.user.conversations.get(id=pk)
    messages = conversation.messages.all()

    # Mark this conversation read by the requesting user
    if request.user in conversation.unread_by.all():
        conversation.unread_by.remove(request.user)
    # TODO: Pagination
    # Logic for creating a new message in a conversation
    if request.method == 'POST':
        # Redirect to unpermitted page if not logged in.
        if not request.user.is_authenticated:
            return unpermitted_view(request)
        form = MessageForm(request, request.POST)
        if form.is_valid():
            new_unread = conversation.users.exclude(id=request.user.id)
            conversation.unread_by.add(*new_unread)
            conversation.save()
            form.save(conversation=conversation)
            return redirect(conversation.get_absolute_url())
    else:
        form = MessageForm(request)
    context = {
        'conversation': conversation,
        'messages': messages,
        'message_form': form
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/conversation_view.html'.format(BOARD_THEME),
        context
    )


def reports_list(request):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned or is not an admin
    if not request.user.is_authenticated or \
        not request.user.is_staff or request.user.is_banned:
        return unpermitted_view(request)
    context = {
        'reports': Report.objects.all()
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/reports_list.html'.format(BOARD_THEME),
        context
    )


def report_view(request, pk):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned or is not an admin
    if not request.user.is_authenticated or \
        not request.user.is_staff or request.user.is_banned:
        return unpermitted_view(request)
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
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/report_view.html'.format(BOARD_THEME),
        context
    )


def report_create(request, thread=None, post=None):
    context = {}
    if thread:
        thread_obj = Thread.objects.get(id=thread)
        context.update({'thread': thread_obj})
    if post:
        post_obj = Post.objects.get(id=post)
        context.update({'post': post_obj})
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.is_banned:
        return unpermitted_view(request)
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
    context.update({'form': form})
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/report_create_form.html'.format(BOARD_THEME),
        context
    )


def members_list(request):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.is_banned:
        return unpermitted_view(request)
    users = EmailUser.objects.order_by('username')
    context = {
        'users': users
    }
    context.update(base_context(request))
    return render(
        request,
        'board/themes/{}/members_list.html'.format(BOARD_THEME),
        context
    )
