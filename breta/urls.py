from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from accounts.api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^$', 'core.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),

    url(r'^api/v1/', include(router.urls)),
)
