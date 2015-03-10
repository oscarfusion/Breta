from .models import Milestone


class BasePermission:
    old = None
    new = None
    user = None

    def __init__(self, old, new, user):
        self.old = old
        self.new = new
        self.user = user


class MilestonePermissions(BasePermission):
    def can_change_status_to_accepted(self):
        return (self.old.status == Milestone.STATUS_ACCEPTED_BY_PM and self.new.status == Milestone.STATUS_ACCEPTED and
                self.new.project.user == self.user)

    def can_change_status_to_pm_accepted(self):
        return (self.new.status == Milestone.STATUS_ACCEPTED_BY_PM and
                self.old.status == Milestone.STATUS_COMPLETE and
                self.new.project.manager == self.user)
