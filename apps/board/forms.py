from django import forms
from django.shortcuts import redirect
from .models import Thread, Post, Shout


class ThreadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['class'] = 'post-editor'

    class Meta:
        model = Thread
        fields = ['title', 'content']


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['class'] = 'post-editor'

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
