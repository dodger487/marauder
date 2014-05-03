from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ('^user', include('accounts.urls')),
    ('^dashboard', include('dashboard.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
    # Examples:
    # url(r'^$', 'marauder.views.home', name='home'),
    # url(r'^marauder/', include('marauder.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    ('^admin/', include(admin.site.urls)),
)
