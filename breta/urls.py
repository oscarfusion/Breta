from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from accounts.api import views as account_views
from core.api import views as core_views

router = routers.DefaultRouter()
router.register(r'users', account_views.UserViewSet)
router.register(r'regions', core_views.RegionViewSet)
router.register(r'cities', core_views.CityViewSet)

urlpatterns = patterns(
    '',
    url(r'^$', 'core.views.home', name='home'),
    url(r'^signup/$', 'accounts.views.signup', name='signup'),
    url(r'^signin/$', 'accounts.views.signin', name='signin'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/v1/', include(router.urls)),
)
