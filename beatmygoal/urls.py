from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import core.views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'beatmygoal.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', core.views.test),
                       url(r'^admin/', include(admin.site.urls)),
)
