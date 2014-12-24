from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

from .models import User


class SignupForm(forms.ModelForm):
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput, required=True, validators=[validators.MinLengthValidator(6)])
    city = forms.CharField(label=_("City"), required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')

    def save(self, *args, **kwargs):
        user = super(SignupForm, self).save(*args, **kwargs)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.save()
        return user


class SigninForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid Email or Password")
            elif not user.is_active:
                raise forms.ValidationError("Your account is not active")

        return self.cleaned_data
