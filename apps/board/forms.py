from django import forms
from .models import Thread, Post, Shout


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


class ShoutForm(forms.ModelForm):
    class Meta:
        model = Shout
        fields = ['content']
