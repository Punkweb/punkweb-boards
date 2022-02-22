from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from punkweb_boards.conf.settings import (
    SIGNATURES_ENABLED,
)
from punkweb_boards.models import (
    Thread,
    Post,
    Shout,
    Report,
    Message,
    Subcategory,
    Category,
)


class KeywordSearchForm(forms.Form):
    keyword = forms.CharField(max_length=80, required=True, label="")


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        widget=forms.TextInput(attrs={"class": "pw-input", "autofocus": True})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "pw-input",
            }
        ),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }


class RegistrationForm(forms.Form):
    username = forms.RegexField(
        regex=r"^\w+$",
        widget=forms.TextInput(
            attrs={"required": True, "max_length": 30, "class": "pw-input"}
        ),
        label=_("Username"),
        error_messages={
            "invalid": _(
                "This value must contain only letters, numbers and underscores."
            )
        },
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "required": True,
                "max_length": 30,
                "render_value": False,
                "class": "pw-input",
            }
        ),
        label=_("Password"),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "required": True,
                "max_length": 30,
                "render_value": False,
                "class": "pw-input",
            }
        ),
        label=_("Password (again)"),
    )

    def clean_username(self):
        try:
            user = get_user_model().objects.get(
                username__iexact=self.cleaned_data["username"]
            )
        except get_user_model().DoesNotExist:
            return self.cleaned_data["username"]

        raise forms.ValidationError(
            _("The username already exists. Please try another one.")
        )

    def clean(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_("The two password fields did not match."))

        return self.cleaned_data


class SettingsForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields["image"].initial = request.user.profile.image
        self.fields["gender"].initial = request.user.profile.gender
        self.fields["birthday"].initial = request.user.profile.birthday
        if SIGNATURES_ENABLED:
            signature = forms.CharField(
                widget=forms.Textarea(attrs={"class": "post-editor"}),
                label=_("Signature"),
                required=False,
                initial=request.user.profile.signature,
            )
            self.fields["signature"] = signature

    GENDER_CHOICES = [("", ""), ("f", "Female"), ("m", "Male")]
    image = forms.ImageField(label=_("Profile Image"), required=False)
    gender = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"required": False}),
        choices=GENDER_CHOICES,
        label=_("Gender"),
        required=False,
    )
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={"class": "pw-input"}),
        label=_("Birthday (yyyy-mm-dd)"),
        required=False,
    )
    # birthday = forms.CharField(
    #     widget=forms.SelectDateWidget(
    #         attrs={
    #             "required": False,
    #             "class": "pw-input",
    #         }
    #     ),
    # )


class ThreadForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields["content"].label = ""
        self.fields["content"].widget.attrs["class"] = "post-editor"
        self.fields["title"].widget.attrs["class"] = "pw-input"
        self.fields["tags"].widget.attrs["class"] = "pw-input"

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
        fields = ["title", "tags", "content"]


class PostForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields["content"].label = ""
        self.fields["content"].widget.attrs["class"] = "post-editor"

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
        fields = ["content"]


class ConversationForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super(ConversationForm, self).__init__(*args, **kwargs)

    users = forms.CharField(
        max_length=240,
        required=True,
        help_text="""
        List of usernames separated by a comma, spaces are fine
    """,
    )
    subject = forms.CharField(max_length=140, initial="No subject")
    message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "post-editor"}),
        label=_("Message"),
        required=True,
    )


class MessageForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields["content"].label = ""
        self.fields["content"].widget.attrs["class"] = "post-editor"
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
        fields = ["content"]


class ShoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShoutForm, self).__init__(*args, **kwargs)
        self.fields["content"].label = ""
        self.fields["content"].widget.attrs["class"] = "shout-editor"

    class Meta:
        model = Shout
        fields = ["content"]


class ReportForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields["reason"].label = "Reason for report:"
        self.fields["reason"].widget.attrs["cols"] = "80"
        self.fields["reason"].widget.attrs["rows"] = "6"
        self.fields["reason"].widget.attrs["class"] = "pw-input"

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
        fields = ["reason"]


class SubcategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubcategoryForm, self).__init__(*args, **kwargs)
        self.fields["parent"].label = "Category"
        self.fields["description"].widget.attrs["class"] = "post-editor"

    class Meta:
        model = Subcategory
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["class"] = "post-editor"

    class Meta:
        model = Category
        fields = "__all__"
