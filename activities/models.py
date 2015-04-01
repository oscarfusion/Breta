from django.db import models

from accounts.models import User
from projects.models import Project, Task, Milestone


class Activity(models.Model):
    class Meta:
        verbose_name_plural = 'Activities'

    TYPE_NEW_PROJECT = 'new-project'
    TYPE_NEW_TASK = 'new-task'
    TYPE_NEW_MILESTONE = 'new-milestone'
    TYPE_TASK_STATUS_CHANGED = 'task-status-changed'
    TYPE_MILESTONE_STATUS_CHANGED = 'milestone-status-changed'
    TYPE_PROJECT_COMPLETED = 'project-completed'
    TYPE_MILESTONE_ACCEPTED = 'milestone-accepted'
    TYPE_MILESTONE_ACCEPTED_BY_PM = 'milestone-accepted-by-pm'

    TYPE_CHOICES = (
        (TYPE_NEW_PROJECT, 'New project created'),
        (TYPE_NEW_TASK, 'New task created'),
        (TYPE_NEW_MILESTONE, 'New milestone created'),
        (TYPE_TASK_STATUS_CHANGED, 'Task status changed'),
        (TYPE_MILESTONE_STATUS_CHANGED, 'Milestone status changed'),
        (TYPE_PROJECT_COMPLETED, 'Project completed'),
        (TYPE_MILESTONE_ACCEPTED, 'Milestone accepted'),
        (TYPE_MILESTONE_ACCEPTED_BY_PM, 'Milestone accepted by PM'),
    )

    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    user = models.ForeignKey(User, related_name='activities', null=True, blank=True)
    project = models.ForeignKey(Project, related_name='project_activities', null=True, blank=True)
    milestone = models.ForeignKey(Milestone, null=True, blank=True)
    task = models.ForeignKey(Task, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null=True, blank=True)

    def __unicode__(self):
        if not self.project:
            return '%d - %s' % (self.id, self.type)
        return '%s - %s - %d' % (self.project.name, self.type, self.id)
