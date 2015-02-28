from core.email import send_email


def send_new_project_email(project):
    return send_email([project.user.email], 'Thank you for submitting new project', 'emails/projects/new_project.html', {'project': project})


def send_manager_assigned_email(project):
    return send_email([project.user.email], 'Manager assigned to your project', 'emails/projects/manager_assigned.html', {'project': project})
