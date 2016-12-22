from django import forms
from .models import Thread, Post, Shout


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        exclude = ['category', 'user']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['thread', 'user']


class ShoutForm(forms.ModelForm):
    class Meta:
        model = Shout
        exclude = ['user']
