from django import forms
from .models import Post, Comment, Shout


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['category', 'user']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post', 'user']


class ShoutForm(forms.ModelForm):
    class Meta:
        model = Shout
        exclude = ['user']
