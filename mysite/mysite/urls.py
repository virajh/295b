from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^erx/', include('erx.urls', namespace='erx')),
                       url(r'^admin/', include(admin.site.urls)),
                       )
