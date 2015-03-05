from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


class ResetPasswordConfirmForm(SetPasswordForm):
    uid = forms.CharField(max_length=255, required=True, )
    token = forms.CharField(max_length=255, required=True)

    def get_user(self):
        _uid = force_text(urlsafe_base64_decode(self.cleaned_data['uid']))
        return get_user_model().objects.get(pk=_uid)

    def clean_uid(self):
        uid = self.cleaned_data['uid']
        try:
            _uid = force_text(urlsafe_base64_decode(uid))
            get_user_model().objects.get(pk=_uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            raise ValidationError('UID is not valid!')
        return uid

    def clean_token(self):
        uid = self.cleaned_data['uid']
        token = self.cleaned_data['token']
        try:
            user = self.get_user()
        except get_user_model().DoesNotExist:
            user = None
        if user is None or not default_token_generator.check_token(user, token):
            raise ValidationError('Token is not valid!')
        return token

    def save(self, commit=True):
        self.user = self.get_user()
        super(ResetPasswordConfirmForm, self).save(commit)
