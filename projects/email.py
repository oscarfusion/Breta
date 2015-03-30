from core.email import send_email


def send_new_project_email(project):
    return send_email([project.user.email], 'Thank you for submitting new project', 'emails/projects/new_project.html', {'project': project})


def send_manager_assigned_email(project):
    return send_email([project.user.email], 'Manager assigned to your project', 'emails/projects/manager_assigned.html', {'project': project})


def send_brief_ready_email(project):
    return send_email([project.user.email], 'Brief and mockups for your project are ready!', 'emails/projects/brief_ready.html', {'project': project})


def send_project_assigned_email(project):
    assert project.manager, 'Project manager should be assigned'
    return send_email([project.manager.email], 'New project assigned to you', 'emails/projects/project_assigned.html', {'project': project})


def send_developer_invited_to_project_email(project_member, message):
    return send_email([project_member.member.email], 'You was invited to project', 'emails/projects/developer_invited.html', {'project_member': project_member, 'message': message})


def send_bids_entered_email(project):
    return send_email([project.user.email], 'Bids for your project are entered', 'emails/projects/bids_entered.html', {'project': project})


def send_quote_accepted_email_to_project_owner(project):
    return send_email([project.user.email], 'Thank you for approving project bid', 'emails/projects/quote_accepted_project_owner.html', {'project': project})


def send_quote_accepted_email_to_developer(project_member):
    return send_email([project_member.member.email], 'Your bid was accepted', 'emails/projects/quote_accepted_developer.html', {'project_member': project_member})


def send_milestone_completed_email(milestone):
    return send_email([milestone.project.user.email], 'Milestone completed', 'emails/projects/milestone_completed.html', {'milestone': milestone})


def send_project_completed_email(project):
    from .models import ProjectMember
    emails = [project.user.email, project.manager.email]
    for member in project.memberships.filter(status=ProjectMember.STATUS_ACCEPTED):
        emails.append(member.member.email)
    return send_email(emails, 'Project is completed', 'emails/projects/project_completed.html', {'project': project})


def send_milestone_due_today(milestone):
    return send_email([milestone.project.manager.email], 'Milestone due', 'emails/projects/milestone_due_today.html', {'milestone': milestone})


def send_milestone_accepted_by_pm_email(milestone):
    return send_email([milestone.project.user.email], 'Milestone "{}"" is accepted by project manager'.format(milestone.name), 'emails/projects/milestone_accepted_by_pm.html', {'milestone': milestone})
