from . import email


def notify_about_new_task_comment(message):
    assert message.task, 'Message should has attached task'
    project_owner = message.task.milestone.project.user
    developer = message.task.milestone.assigned
    user_to_notify = developer if message.sender == project_owner else project_owner
    return email.send_new_task_comment_email(user_to_notify, message.task)


def notify_about_new_milestone_comment(message):
    assert message.milestone, 'Message should has attached milestone'
    project_owner = message.milestone.project.user
    developer = message.milestone.assigned
    user_to_notify = developer if message.sender == project_owner else project_owner
    return email.send_new_milestone_comment_email(user_to_notify, message.milestone)
