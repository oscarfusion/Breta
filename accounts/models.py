from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext as _
from djorm_pgarray.fields import ArrayField
from rest_framework.authtoken.models import Token
from bitfield import BitField


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


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)

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

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.get_full_name()

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


@receiver(post_save, sender=User)
def init_new_user(sender, instance, signal, created, **kwargs):
    """
    Create an authentication token for newly created users.
    """
    if created:
        Token.objects.create(user=instance)


def avatar_upload_to(instance, filename):
    return 'avatars/%d - %s' % (instance.id, filename)


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
        ('lorem', 'Lorem',),
        ('sit_amet_consecteur', 'Sit Amet Consecteur',),
        ('ipsum_dolor', 'Ipsum Dolor',),
        ('adiposcing_elit', 'Adiposcing Elit',),
    )

    user = models.ForeignKey(User, unique=True, related_name='developer')
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, default=DEVELOPER)
    title = models.CharField(max_length=255)
    bio = models.TextField()
    skills = ArrayField(dbtype='varchar')
    availability = models.CharField(max_length=255, choices=AVAILABLE_CHOICES, default=AVAILABLE_NOW)
    project_preferences = BitField(flags=PROJECT_PREFERENCES_FLAGS)
    avatar = models.FileField(upload_to=avatar_upload_to, blank=True, null=True)
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
