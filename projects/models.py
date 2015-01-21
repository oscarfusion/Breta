from django.db import models
from django.utils.text import slugify
from accounts.models import User


class Project(models.Model):
    WEBSITE = 'WS'
    APP = 'APP'
    WEBSITE_AND_APP = 'WAA'

    PROJECT_CHOICES = (
        (WEBSITE, 'Website'),
        (APP, 'App'),
        (WEBSITE_AND_APP, 'Website & App'),
    )

    project_type = models.CharField(max_length=255, choices=PROJECT_CHOICES, default=WEBSITE)
    name = models.CharField(max_length=255)
    idea = models.CharField(max_length=255)
    description = models.TextField()
    price_range = models.CharField(max_length=255)
    is_sure_about_price = models.BooleanField(default=False)
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
