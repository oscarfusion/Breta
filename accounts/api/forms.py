from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import get_user_model

from ..models import Email
from .. import email


class ResetPasswordForm(PasswordResetForm):
    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        UserModel = get_user_model()()
        email_val = self.cleaned_data["email"]
        active_users = UserModel._default_manager.filter(
            email__iexact=email_val, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            email.send_password_reset_email(email_val, c)


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


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('email', 'from_landing')


class InviteUserForm(forms.Form):
    email = forms.EmailField(required=True)
    referral_link = forms.CharField(required=True)

    def save(self, *args, **kwargs):
        email.send_invite_email(self.cleaned_data['email'], self.cleaned_data['referral_link'])
