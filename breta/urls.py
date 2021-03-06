from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from accounts.api import views as account_views
from activities.api import views as activity_views
from breta_messages.api import views as message_views
from core.api import views as core_views
from projects.api import views as project_views
from payments.api import views as payments_views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'activities', activity_views.ActivityViewSet)
router.register(r'users', account_views.UserViewSet)
router.register(r'users-search', account_views.UsersSearchViewSet)
router.register(r'developers', account_views.DeveloperViewSet)
router.register(r'portfolio-projects', account_views.PortfolioProjectViewSet)
router.register(r'portfolio-project-attachments', account_views.PortfolioProjectAttachmentViewSet)
router.register(r'websites', account_views.WebsiteViewSet)
router.register(r'emails', account_views.EmailViewSet)
router.register(r'regions', core_views.RegionViewSet)
router.register(r'cities', core_views.CityViewSet)
router.register(r'projects', project_views.ProjectViewSet)
router.register(r'project-files', project_views.ProjectFileViewSet)
router.register(r'milestones', project_views.MilestoneViewSet)
router.register(r'tasks', project_views.TaskViewSet)
router.register(r'project-messages', project_views.ProjectMessageViewSet)
router.register(r'project-members', project_views.ProjectMemberViewSet)
router.register(
    r'messages/inbox-messages',
    message_views.InboxMessagesCount,
    base_name='inbox-messages-amount'
)
router.register(
    r'messages/unread-messages',
    message_views.UnreadMessageViewSet,
    base_name='unread-messages'
)
router.register(r'messages', message_views.MessageViewSet)
router.register(r'message-files', message_views.MessageFileViewSet)
router.register(r'message-recipients', message_views.MessageRecipientViewSet)
router.register(
    r'credit-cards/has-active-card',
    payments_views.UserHasActiveCreditCardViewSet,
    base_name='active-credit-card'
)
router.register(r'credit-cards', payments_views.CreditCardViewSet)
router.register(r'payout-methods', payments_views.PayoutMethodViewSet)
router.register(r'transactions', payments_views.TransactionViewSet)
router.register(r'user-balances', payments_views.UsersBalancesViewSet, base_name='user-balance')
router.register(r'quotes', project_views.QuoteViewSet)


urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^signup/$', 'accounts.views.signup', name='signup'),
    url(r'^signin/$', 'accounts.views.signin', name='signin'),
    url(r'^stripe/$', 'core.views.stripe_test', name='stripe_test'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-token-auth/', 'core.api.views.obtain_auth_token'),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/config/', 'core.api.views.breta_config'),
    url(r'^api/v1/change-password/', account_views.ChangePasswordView.as_view()),
    url(r'^api/v1/reset-password/$', account_views.ResetPasswordView.as_view()),
    url(r'^api/v1/reset-password/confirm/', account_views.ResetPasswordConfirmView.as_view()),
    url(r'^api/v1/invite-user/', account_views.InvityByEmailView.as_view()),
    url(r'^tinymce/', include('tinymce.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
