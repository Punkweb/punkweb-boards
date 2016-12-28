from django.shortcuts import render
from django.http import Http404
from apps.board.models import Category, Subcategory, Thread, Post, Shout
from apps.board.forms import ShoutForm


def portal_view(request):
    context = {
    }
    return render(request, 'portal.html', context)
