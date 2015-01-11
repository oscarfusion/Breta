from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from accounts.api import views as account_views
from breta_messages.api import views as message_views
from core.api import views as core_views
from projects.api import views as project_views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', account_views.UserViewSet)
router.register(r'regions', core_views.RegionViewSet)
router.register(r'cities', core_views.CityViewSet)
router.register(r'projects', project_views.ProjectViewSet)
router.register(r'project-files', project_views.ProjectFileViewSet)
router.register(r'messages', message_views.MessageViewSet)
router.register(r'message-files', message_views.MessageFileViewSet)
router.register(r'message-recipients', message_views.MessageRecipientViewSet)

urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^signup/$', 'accounts.views.signup', name='signup'),
    url(r'^signin/$', 'accounts.views.signin', name='signin'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api-token-auth/', 'core.api.views.obtain_auth_token'),
    url(r'^api/v1/', include(router.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
