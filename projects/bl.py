from . import email


def quote_submitted_to_project_owner(quote):
    from .models import Quote
    project = quote.project_member.project
    developer = quote.project_member.developer.first()
    submitted_quotes_count = Quote.objects.filter(
        Quote.condition_status_project(project),
        Quote.condition_status_developer_type(developer.type),
        Quote.condition_status_owner_pending(),
    ).count()
    print 'submitted_quotes_count', submitted_quotes_count
    if submitted_quotes_count == 3:
        email.send_bids_entered_email(quote.project_member)
