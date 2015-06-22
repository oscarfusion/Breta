import os
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext as _
from djorm_pgarray.fields import ArrayField
from djorm_pgjson.fields import JSONField
from multiselectfield import MultiSelectField
from rest_framework.authtoken.models import Token
from bitfield import BitField

from . import email
from . import mailchimp_api


class UserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


def avatar_upload_to(instance, filename):
    return 'avatars/%d - %s' % (instance.id, filename)


def get_referral_code():
    return str(uuid.uuid4())


class User(AbstractBaseUser, PermissionsMixin):
    PROJECT_OWNER = 'project-owner'
    DEVELOPER = 'developer'
    OTHER = 'other'

    USER_TYPES = (
        (PROJECT_OWNER, 'Project Owner'),
        (DEVELOPER, 'Developer'),
        (OTHER, 'Other'),
    )

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    location = models.CharField(max_length=255, blank=True, null=True)

    city = models.ForeignKey('cities_light.City', blank=True, null=True)

    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'), default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    avatar = models.FileField(upload_to=avatar_upload_to, blank=True, null=True)
    referral_code = models.CharField(max_length=255, blank=True, null=True)
    referrer = models.ForeignKey('self', related_name='invited_users', blank=True, null=True)
    referrer_email = models.EmailField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    settings = JSONField()
    paypal_email = models.EmailField(blank=True, null=True)
    signup_completed = models.BooleanField(default=False)
    user_type = models.CharField(max_length=255, choices=USER_TYPES, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    __original_is_active = None

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__original_is_active = self.is_active

    def __unicode__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = get_referral_code()
        if self.__original_is_active is False and self.is_active is True:
            email.send_account_activated_email(self)
        super(User, self).save(*args, **kwargs)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def payout_method_exists(self):
        return self.payout_methods.count() > 0

    @property
    def safe_settings(self):
        return self.settings if isinstance(self.settings, dict) else {}


@receiver(post_save, sender=User)
def init_new_user(sender, instance, signal, created, **kwargs):
    """
    Create an authentication token for newly created users.
    """
    if created:
        Token.objects.create(user=instance)


class Developer(models.Model):
    DEVELOPER = 'DEV'
    DESIGNER = 'DES'
    TYPE_CHOICES = (
        (DEVELOPER, 'Developer'),
        (DESIGNER, 'Designer'),
    )

    AVAILABLE_NOW = 'NOW'
    AVAILABLE_CHOICES = (
        (AVAILABLE_NOW, 'Now'),
    )

    PROJECT_PREFERENCES_FLAGS = (
        ('small', 'Small',),
        ('big', 'Big',),
    )

    user = models.ForeignKey(User, unique=True, related_name='developer')
    type = MultiSelectField(choices=TYPE_CHOICES, default=DEVELOPER, blank=True, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    skills = ArrayField(dbtype='varchar')
    availability = models.CharField(max_length=255, choices=AVAILABLE_CHOICES, default=AVAILABLE_NOW)
    project_preferences = BitField(flags=PROJECT_PREFERENCES_FLAGS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.get_full_name()


class Website(models.Model):
    WEBSITE = 1
    GITHUB = 2

    TYPE_CHOICES = (
        (WEBSITE, 'Website'),
        (GITHUB, 'Github')
    )

    developer = models.ForeignKey(Developer, related_name='websites')
    type = models.IntegerField(max_length=255, choices=TYPE_CHOICES, default=WEBSITE)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.url


def portfolio_project_file_upload_to(instance, filename):
    return 'portfolio_files/%d/%s' % (instance.id, filename)


def portfolio_project_attachment_file_upload_to(instance, filename):
    return 'portfolio_files/%d/%s' % (instance.project.id, filename)


class PortfolioProject(models.Model):
    developer = models.ForeignKey(Developer, related_name='portfolio_projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    website = models.CharField(max_length=255)
    image = models.FileField(upload_to=portfolio_project_file_upload_to, blank=True, null=True)
    skills = ArrayField(dbtype='varchar')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class PortfolioProjectAttachment(models.Model):
    project = models.ForeignKey(PortfolioProject, related_name='attachments')
    file = models.FileField(upload_to=portfolio_project_attachment_file_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s - %s' % (self.project.title, self.file)

    @property
    def filename(self):
        return os.path.basename(self.file.name)


class Email(models.Model):
    class Meta:
        verbose_name_plural = 'Newsletter signups'
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Joined date')
    referral_code = models.CharField(max_length=255, blank=True, null=True)
    from_landing = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = get_referral_code()
        if not self.pk:
            mailchimp_api.subscribe_by_email(self.email)
            if self.from_landing:
                email.send_user_subscribed_email(self.email)
        super(Email, self).save(*args, **kwargs)


@receiver(post_save, sender=Email)
def email_post_save(sender, instance, signal, created, **kwargs):
    if created:
        mailchimp_api.subscribe_by_email(instance.email)
