from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Conversation, Message


def conversations_list(request):
    conversations = request.user.conversations.all()
    context = {
        'conversations': conversations
    }
    return render(request, 'conversations/conversations_list.html', context)


class ConversationUpdate(UpdateView):
    model = Conversation
    fields = ['users', 'subject']
    template_name_suffix = '_update_form'


class ConversationDelete(DeleteView):
    model = Conversation
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('board:index')


class MessageCreate(CreateView):
    model = Message
    fields = ['content']
    template_name_suffix = '_create_form'


class MessageUpdate(UpdateView):
    model = Message
    fields = ['content']
    template_name_suffix = '_update_form'


class MessageDelete(DeleteView):
    model = Message
    template_name_suffix = '_delete_form'
    success_url = reverse_lazy('board:index')
