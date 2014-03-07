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
	url(r'^goals/create', core.views.goal_create_goal, name='goal_create_goal'),
	url(r'^goals/delete', core.views.goal_delete_goal, name='goal_create_goal'),
	url(r'^users/(\d)/edit', core.views.edit_user, name='edit_user'),
	url(r'^users/test', core.views.test_user, name='test_user'),

)
