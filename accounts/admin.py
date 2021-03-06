from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple
from bitfield.admin import BitFieldListFilter
from multiselectfield import MultiSelectField, MultiSelectFormField

from .models import User, Developer, Website, PortfolioProject, PortfolioProjectAttachment


class AdminUserCreationForm(UserCreationForm):
    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = None
    email = forms.EmailField(label=_("Email"), max_length=255)
    password1 = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )


class AdminUserChangeForm(UserChangeForm):
    username = None
    email = forms.EmailField(label=_("Email"), max_length=255)


class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'location', 'avatar', 'referral_code', 'referrer_email', 'ip_address', 'paypal_email', 'user_type')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'signup_completed',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm

    def get_queryset(self, request):
        return User.objects.defer('settings').all()


class WebsiteInline(admin.StackedInline):
    extra = 1
    model = Website


class PortfolioProjectInline(admin.StackedInline):
    extra = 1
    model = PortfolioProject


class PortfolioProjectAttachmentInline(admin.StackedInline):
    extra = 1
    model = PortfolioProjectAttachment


class DeveloperAdmin(admin.ModelAdmin):
    inlines = [WebsiteInline, PortfolioProjectInline]
    list_display = ('user', 'type', 'created_at', 'updated_at',)
    search_fields = ('type',)

    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
        MultiSelectField: {'widget': MultiSelectFormField},
    }

    list_filter = (
        ('project_preferences', BitFieldListFilter,),
    )


class EmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'ip_address',)
    readonly_fields = ('created_at', 'ip_address',)


admin.site.register(User, UserAdmin)
admin.site.register(Developer, DeveloperAdmin)
