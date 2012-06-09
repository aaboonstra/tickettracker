from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import redirect_to
admin.autodiscover()

from tools.login import LoginView

urlpatterns = patterns('',
#    (r'^$', redirect_to, {'url': '/o/'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
#    ('^o/', include('management.apps.overview.urls', namespace='overview')),

    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)
