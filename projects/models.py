from django.db import models
from django.utils.text import slugify
from accounts.models import User


class Project(models.Model):
    WEBSITE = 'WS'
    TABLET_APP = 'TA'
    PHONE_APP = 'PA'
    DESKTOP_PROGRAM = 'DP'

    PROJECT_CHOICES = (
        (WEBSITE, 'Website'),
        (TABLET_APP, 'Tablet app'),
        (PHONE_APP, 'Phone app'),
        (DESKTOP_PROGRAM, 'Desktop program')
    )

    ONE_TO_FIVE = '1-5'
    FIVE_TO_TEN = '5-10'

    PRICE_RANGES = (
        (ONE_TO_FIVE, '$1000-5000'),
        (FIVE_TO_TEN, '$5000-10000')
    )

    project_type = models.CharField(max_length=255, choices=PROJECT_CHOICES, default=WEBSITE)
    name = models.CharField(max_length=255)
    idea = models.CharField(max_length=255)
    description = models.TextField()
    price_range = models.CharField(max_length=255, choices=PRICE_RANGES, default=ONE_TO_FIVE)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)

    def files(self):
        return ProjectFile.objects.filter(project=self)

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.name))
        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


def file_upload_to(instance, filename):
    return 'project_files/%s/%s' % (instance.project.slug, filename)


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, related_name='files')
    file = models.FileField(upload_to=file_upload_to)

    def __unicode__(self):
        return '%s - %s' % (self.project.name, self.file)
