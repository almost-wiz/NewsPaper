from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        login_field = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "placeholder": _("Login or e-mail"),
                    "autocomplete": "username_email",
                    "class": "form-control",
                    "id": "login"
                }
            ),
        )
        password_field = forms.CharField(
            widget=forms.PasswordInput(
                attrs={
                    "placeholder": _("Password"),
                    "autocomplete": "current-password",
                    "class": "form-control",
                    "id": "password"
                }
            ),
        )
        remember = forms.BooleanField(
            required=False,
            widget=forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "id": "remember"
                }
            )
        )

        self.fields["login"] = login_field
        self.fields["password"] = password_field
        self.fields['remember'] = remember


class CustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

        email_field = forms.EmailField(
            widget=forms.TextInput(
                attrs={
                    "type": "email",
                    "placeholder": _("E-mail"),
                    "autocomplete": "email",
                    "class": "form-control",
                    "id": "email",
                }
            ),
        )

        username_field = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "placeholder": _("Login"),
                    "autocomplete": "username",
                    "class": "form-control",
                    "id": "username"
                }
            ),
        )
        password_field1 = forms.CharField(
            widget=forms.PasswordInput(
                attrs={
                    "placeholder": _("Password"),
                    "autocomplete": "current-password",
                    "class": "form-control",
                    "id": "password1"
                }
            ),
        )
        password_field2 = forms.CharField(
            widget=forms.PasswordInput(
                attrs={
                    "placeholder": _("Repeat password"),
                    "autocomplete": "current-password",
                    "class": "form-control",
                    "id": "password2"
                }
            ),
        )
        self.fields["email"] = email_field
        self.fields["username"] = username_field
        self.fields["password1"] = password_field1
        self.fields["password2"] = password_field2

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
