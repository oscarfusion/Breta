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
