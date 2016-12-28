import datetime
from django import forms
from django.shortcuts import redirect
from .models import Thread, Post, Shout


class ThreadForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['content'].widget.attrs['class'] = 'post-editor'

    def save(self, category=None, commit=True, set_user=False):
        obj = super(ThreadForm, self).save(commit=False)
        if category:
            obj.category = category
        if set_user:
            obj.user = self.request.user
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Thread
        fields = ['title', 'content']


class PostForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['content'].widget.attrs['class'] = 'post-editor'

    def save(self, thread=None, commit=True, set_user=False):
        obj = super(PostForm, self).save(commit=False)
        if thread:
            obj.thread = thread
            obj.thread.modified = datetime.datetime.now()
        if set_user:
            obj.user = self.request.user
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Post
        fields = ['content']


class ShoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShoutForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['class'] = 'shout-editor'

    class Meta:
        model = Shout
        fields = ['content']
