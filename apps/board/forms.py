from django import forms
from .models import Post, Shout


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['category', 'user']


class ShoutForm(forms.ModelForm):
    class Meta:
        model = Shout
        exclude = ['user']
