from django.db.models import Q
from django.utils import timezone

from breta.celery import app
from . import email
from .models import Milestone


@app.task()
def milestones_due_today():
    milestones = Milestone.objects.filter(
        Q(due_date=timezone.now().date()) &
        Q(is_due_email_sent=False) &
        ~Q(status=Milestone.STATUS_ACCEPTED)
    )
    for milestone in milestones:
        email.send_milestone_due_today(milestone)
        milestone.is_due_email_sent = True
        milestone.save()
