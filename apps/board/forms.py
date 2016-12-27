from django import forms
from .models import Category, Subcategory, Thread, Post, Shout


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['class'] = 'category-editor'

    class Meta:
        model = Category
        fields = ['name', 'description', 'order', 'auth_req']


class SubcategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubcategoryForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['class'] = 'category-editor'

    class Meta:
        model = Subcategory
        fields = ['name', 'description', 'order', 'admin_req', 'auth_req']


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
