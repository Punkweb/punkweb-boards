from django.shortcuts import render


def portal_view(request):
    context = {
    }
    return render(request, 'portal.html', context)
