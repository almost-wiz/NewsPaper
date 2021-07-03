from allauth.account.adapter import DefaultAccountAdapter
from allauth.account import app_settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django import forms


class CustomDefaultAccountAdapter(DefaultAccountAdapter):
    error_messages = {
        "username_blacklisted": _(
            "adasdUsername can not be used. Please use other username."
        ),
        "username_taken": _(
            "Пользователь с таким логином адресом уже есть."
        ),
        "too_many_login_attempts": _(
            "saasddToo many failed login attempts. Try again later."
        ),
        "email_taken": _(
            "Пользователь с таким e-mail адресом уже есть."
        ),
    }

    def clean_password(self, password, user=None):
        min_length = app_settings.PASSWORD_MIN_LENGTH
        if min_length and len(password) < min_length:
            raise forms.ValidationError(
                _("Пароль должен содержать от {0} " "символов.").format(min_length)
            )
        validate_password(password, user)
        return password
