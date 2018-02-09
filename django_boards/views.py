import logging
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector, TrigramSimilarity)
from django.db.models import Q
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django_boards.conf.settings import BOARD_THEME, SIGNATURES_ENABLED
from django_boards.forms import (
    ThreadForm, PostForm, ReportForm, MessageForm, RegistrationForm,
    SettingsForm, KeywordSearchForm)
# from django_boards.models import (
#     EmailUser, Category, Subcategory, Thread, Post, Report, Conversation,
#     Message, Notification, Shout, Page)
from django_boards.models import (
    Category, Subcategory, Thread, Post, Report, Conversation,
    Message, Notification, Shout, Page)


logger = logging.getLogger(__name__)


def unpermitted_view(request):
    return render(
        request, 'django_boards/themes/{}/unpermitted.html'.format(BOARD_THEME), {})


def index_view(request):
    total_posts = Post.objects.all().count()
    total_threads = Thread.objects.all().count()
    last_25_shouts = Shout.objects.all()[:25]

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

    users = get_user_model().objects.select_related('profile').all()
    online = [user for user in users if user.profile.online()]
    online_staff = [user for user in users if user.profile.online() and user.is_staff]
    newest_member = users.order_by('-date_joined').first()
    member_count = users.count()
    context = {
        'total_posts': total_posts,
        'total_threads': total_threads,
        'shouts': last_25_shouts,
        'categories': category_groups,
        'recent_threads': recent_threads[:5],
        'recent_activity': recent_activity[:5],
        'users_online': online,
        'staff_online': online_staff,
        'newest_member': newest_member,
        'member_count': member_count,
    }
    return render(
        request, 'django_boards/themes/{}/index.html'.format(BOARD_THEME), context)


def keyword_search_view(request):
    if not request.user.is_authenticated or request.user.profile.is_banned:
        return redirect('board:unpermitted')

    if request.GET.get('keyword'):
        keyword = request.GET['keyword']
    else:
        keyword = ''

    query = SearchQuery(keyword)

    # Users
    user_trigram = TrigramSimilarity(
        'username', keyword
    ) + TrigramSimilarity(
        'email', keyword
    )
    matched_users = get_user_model().objects.annotate(
        similarity=user_trigram,
    ).filter(similarity__gt=0.3).order_by('-similarity')

    # Threads
    thread_vector = SearchVector(
        'tags', weight='A'
    ) + SearchVector(
        'title', weight='A'
    ) + SearchVector(
        'content', weight='B'
    ) + SearchVector(
        'user__username', weight='C'
    )
    thread_trigram = TrigramSimilarity(
        'title', keyword
    ) + TrigramSimilarity(
        'user__username', keyword
    ) + TrigramSimilarity(
        'tags', keyword
    )
    matched_threads = Thread.objects.annotate(
        search=thread_vector,
        similarity=thread_trigram,
    ).annotate(
        rank=SearchRank(thread_vector, query)
    ).filter(Q(search=query) | Q(similarity__gt=0.15)).order_by('-rank')

    # Posts
    post_vector = SearchVector(
        'content', weight='A',
    ) + SearchVector(
        'user__username', weight='B'
    )
    matched_posts = Post.objects.annotate(
        search=post_vector,
    ).annotate(
        rank=SearchRank(post_vector, query)
    ).filter(search=query).order_by('-rank')

    context = {
        'matched_users': matched_users,
        'matched_threads': matched_threads,
        'matched_posts': matched_posts,
        'keyword': keyword
    }
    return render(
        request,
        'django_boards/themes/{}/keyword_search.html'.format(BOARD_THEME),
        context
    )


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = get_user_model().objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )
            return redirect('/board/login/')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(
        request, 'django_boards/themes/{}/register.html'.format(BOARD_THEME), context)


def my_profile(request):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.profile.is_banned:
        return redirect('board:unpermitted')
    context = {}
    return render(
        request, 'django_boards/themes/{}/my_profile.html'.format(BOARD_THEME), context)


def settings_view(request):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.profile.is_banned:
        return redirect('board:unpermitted')
    if request.method == 'POST':
        form = SettingsForm(request, request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['image']:
                request.user.profile.image = form.cleaned_data['image']
            if form.cleaned_data['gender']:
                request.user.profile.gender = form.cleaned_data['gender']
            if form.cleaned_data['birthday']:
                request.user.profile.birthday = form.cleaned_data['birthday']
            if SIGNATURES_ENABLED and form.cleaned_data['signature']:
                request.user.profile.signature = form.cleaned_data['signature']
            request.user.save()
            return redirect('/board/me/')
    else:
        form = SettingsForm(request)
    context = {
        'form': form
    }
    return render(
        request, 'django_boards/themes/{}/settings.html'.format(BOARD_THEME), context)

# TODO: Don't call the context variable profile
def profile_view(request, username):
    user = get_user_model().objects.get(username=username)
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.profile.is_banned:
        return redirect('board:unpermitted')
    # Redirect to /board/me/ if trying to view own profile.
    if request.user.id == user.id:
        # TODO do not redirect so that users
        # can view their profile as others see it.
        return redirect('board:me')
    context = {
        'profile': user
    }
    return render(
        request,
        'django_boards/themes/{}/profile_page.html'.format(BOARD_THEME),
        context
    )


def category_view(request, pk):
    category = Category.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have view
    # permissions on this category.
    if not category.can_view(request.user):
        return redirect('board:unpermitted')
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
    return render(
        request,
        'django_boards/themes/{}/category_view.html'.format(BOARD_THEME),
        context
    )


def subcategory_view(request, pk):
    category = Subcategory.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have view
    # permissions on this subcategory.
    if not category.can_view(request.user):
        return redirect('board:unpermitted')
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
    return render(
        request,
        'django_boards/themes/{}/subcategory_view.html'.format(BOARD_THEME),
        context
    )


def thread_view(request, pk):
    page_size = 10
    thread = Thread.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have view
    # permissions on this thread.
    if not thread.can_view(request.user):
        return redirect('board:unpermitted')
    # Paginate posts
    paginator = Paginator(thread.posts.order_by('created'), page_size)
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
            return redirect('board:unpermitted')
        form = PostForm(request, request.POST)
        if form.is_valid():
            new_post = form.save(thread=thread, set_user=True)
            # Redirect to this post
            return redirect(new_post)
    else:
        form = PostForm(request)
    context = {
        'thread': thread,
        'posts': posts,
        'post_form': form,
    }
    return render(
        request,
        'django_boards/themes/{}/thread_view.html'.format(BOARD_THEME),
        context
    )


def thread_create(request, category_id):
    subcategory = Subcategory.objects.get(id=category_id)
    # Redirect to unpermitted page if the requesting user does not have post
    # permission in this category.
    if not subcategory.can_post(request.user):
        return redirect('board:unpermitted')
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
    return render(
        request,
        'django_boards/themes/{}/thread_create_form.html'.format(BOARD_THEME),
        context
    )


def thread_update(request, pk):
    instance = Thread.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have edit
    # permissions on this thread.
    if not instance.can_edit(request.user):
        return redirect('board:unpermitted')
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
    return render(
        request,
        'django_boards/themes/{}/thread_update_form.html'.format(BOARD_THEME),
        context
    )


def thread_delete(request, pk):
    instance = Thread.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have edit
    # permissions on this thread.
    if not instance.can_edit(request.user):
        return redirect('board:unpermitted')
    if request.method == 'POST':
        redirect_to = instance.category.id
        instance.delete()
        return redirect('board:subcategory', redirect_to)
    context = {
        'object': instance
    }
    return render(
        request,
        'django_boards/themes/{}/thread_delete_form.html'.format(BOARD_THEME),
        context
    )


# There is no post_view or post_create as both are handled on the thread_view

def post_update(request, pk):
    instance = Post.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have edit
    # permissions on this post.
    if not instance.can_edit(request.user):
        return redirect('board:unpermitted')
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
    return render(
        request,
        'django_boards/themes/{}/post_update_form.html'.format(BOARD_THEME),
        context
    )


def post_delete(request, pk):
    instance = Post.objects.get(id=pk)
    # Redirect to unpermitted page if the requesting user does not have edit
    # permissions on this post.
    if not instance.can_edit(request.user):
        return redirect('board:unpermitted')
    if request.method == 'POST':
        redirect_to = instance.thread.id
        instance.delete()
        return redirect('board:thread', redirect_to)
    context = {
        'object': instance
    }
    return render(
        request,
        'django_boards/themes/{}/post_delete_form.html'.format(BOARD_THEME),
        context
    )


def conversations_list(request):
    # Redirect to unpermitted page if not authenticated or is banned
    if not request.user.is_authenticated or request.user.profile.is_banned:
        return unpermitted_view(request)
    conversations = request.user.conversations.all()
    context = {
        'conversations': conversations
    }
    return render(
        request,
        'django_boards/themes/{}/inbox.html'.format(BOARD_THEME),
        context
    )


def conversation_view(request, pk):
    # Redirect to unpermitted page if not authenticated or is banned
    if not request.user.is_authenticated or request.user.profile.is_banned:
        return redirect('board:unpermitted')
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
            return redirect('board:unpermitted')
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
    return render(
        request,
        'django_boards/themes/{}/conversation_view.html'.format(BOARD_THEME),
        context
    )


def reports_list(request):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned or is not an admin
    if not request.user.is_authenticated or \
        not request.user.is_staff or request.user.profile.is_banned:
        return redirect('board:unpermitted')
    context = {
        'reports': Report.objects.all()
    }
    return render(
        request,
        'django_boards/themes/{}/reports_list.html'.format(BOARD_THEME),
        context
    )


def report_view(request, pk):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned or is not an admin
    if not request.user.is_authenticated or \
        not request.user.is_staff or request.user.profile.is_banned:
        return redirect('board:unpermitted')
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
    return render(
        request,
        'django_boards/themes/{}/report_view.html'.format(BOARD_THEME),
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
    if not request.user.is_authenticated or request.user.profile.is_banned:
        return redirect('board:unpermitted')
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
    return render(
        request,
        'django_boards/themes/{}/report_create_form.html'.format(BOARD_THEME),
        context
    )


def notification_redirect(request, pk):
    notification = Notification.objects.filter(user=request.user, pk=pk)
    if notification:
        notification = notification[0]
        notification.read = True
        notification.save()
        return redirect(notification.link)


def members_list(request):
    # Redirect to unpermitted page if requesting user
    # is not logged in or is banned
    if not request.user.is_authenticated or request.user.profile.is_banned:
        return redirect('board:unpermitted')
    users = get_user_model().objects.filter(profile__is_banned=False).order_by('username')
    context = {
        'users': users
    }
    return render(
        request,
        'django_boards/themes/{}/members_list.html'.format(BOARD_THEME),
        context
    )


def statistics_view(request):
    context = {

    }
    return render(
        request,
        'django_boards/themes/{}/statistics.html'.format(BOARD_THEME),
        context
    )

def page_view(request, slug):
    if not slug:
        return redirect('board:index')
    if request.user.is_authenticated and request.user.profile.is_banned:
        return redirect('board:unpermitted')
    try:
        page = Page.objects.get(slug=slug)
    except Page.DoesNotExist:
        return redirect('pages:not-found')
    context = {
        'page': page,
    }
    return render(
        request, 'django_boards/themes/{}/page.html'.format(BOARD_THEME), context)


def page_not_found_view(request):
    context = {}
    return render(
        request, 'django_boards/themes/{}/page_not_found.html'.format(BOARD_THEME), context)
