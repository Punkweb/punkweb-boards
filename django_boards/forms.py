from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.widgets import ImageClearableFileInput
from django_boards.conf.settings import BOARD_THEME, CAPTCHAS_ENABLED, SIGNATURES_ENABLED
from django_boards.models import Thread, Post, Shout, Report, Message
# from django_boards.models import EmailUser, Thread, Post, Shout, Report, Message


# class NewConversationForm(forms.Form):
#     def __init__(self, request, *args, **kwargs):
#         super(NewConversationForm, self).__init__(*args, **kwargs)
#
#     users_queryset = EmailUser.objects.exclude(is_banned=True)
#     subject = forms.CharField(max_length=140, initial='No subject')
#     users = forms.ModelMultipleChoiceField(queryset=users_queryset)
#     message = forms.CharField(
#         widget=forms.Textarea(attrs={'class': 'post-editor'}),
#         label=_('Message'),
#         required=True
#     )


class KeywordSearchForm(forms.Form):
    keyword = forms.CharField(max_length=80, required=True, label='')


class SettingsForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['gender'].initial = request.user.profile.gender
        self.fields['birthday'].initial = request.user.profile.birthday
        if SIGNATURES_ENABLED:
            signature = forms.CharField(
                widget=forms.Textarea(attrs={'class': 'post-editor'}),
                label=_('Signature'),
                required=False,
                initial=request.user.profile.signature
            )
            self.fields['signature'] = signature

    GENDER_CHOICES = [
        ('', ''),
        ('f', 'Female'),
        ('m', 'Male'),
    ]
    image = forms.ImageField(
        label=_('Profile Image'),
        required=False
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label=_('Gender'),
        required=False
    )
    birthday = forms.DateField(
        label=_('Birthday (yyyy-mm-dd)'),
        required=False
    )


class RegistrationForm(forms.Form):
    username = forms.RegexField(
        regex=r'^\w+$',
        widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
        label=_("Username"),
        error_messages={
            'invalid': _("This value must contain only letters, " \
                         "numbers and underscores.")
        }
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
        label=_("Email address")
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Password")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Password (again)")
    )
    if CAPTCHAS_ENABLED:
        from captcha.fields import CaptchaField
        captcha = CaptchaField()

    def clean_username(self):
        try:
            user = get_user_model().objects.get(
                username__iexact=self.cleaned_data['username'])
        except get_user_model().DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. " \
                                      "Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and \
           'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(
                    _("The two password fields did not match."))
        return self.cleaned_data


class ThreadForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['content'].label = ''
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
        fields = ['title', 'tags', 'content']


class PostForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['content'].label = ''
        self.fields['content'].widget.attrs['class'] = 'post-editor'

    def save(self, thread=None, commit=True, set_user=False):
        obj = super(PostForm, self).save(commit=False)
        if thread:
            obj.thread = thread
            obj.thread.modified = timezone.now()
            obj.thread.save()
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
        self.fields['content'].label = ''
        self.fields['content'].widget.attrs['class'] = 'shout-editor'

    class Meta:
        model = Shout
        fields = ['content']


class ReportForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['reason'].label = 'Reason for report:'
        self.fields['reason'].widget.attrs['cols'] = '80'
        self.fields['reason'].widget.attrs['rows'] = '6'

    def save(self, thread=None, post=None, set_user=False, commit=True):
        obj = super(ReportForm, self).save(commit=False)
        if thread:
            obj.thread = thread
        if post:
            obj.post = post
        if set_user:
            obj.reporting_user = self.request.user
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Report
        fields = ['reason']


class MessageForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = ''
        self.fields['content'].widget.attrs['class'] = 'post-editor'
        self.request = request

    def save(self, conversation=None, commit=True):
        obj = super(MessageForm, self).save(commit=False)
        obj.user = self.request.user
        if conversation:
            obj.conversation = conversation
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Message
        fields = ['content']
