from django import forms
from .models import Thread, Comment, Shout


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        exclude = ['category', 'user']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['thread', 'user']


class ShoutForm(forms.ModelForm):
    class Meta:
        model = Shout
        exclude = ['user']
