from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

import core.views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',

	# Examples:
	# url(r'^$', 'beatmygoal.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	url(r'^$', core.views.index),
	url(r'^admin/', include(admin.site.urls)),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
	url(r'^goals/create', core.views.goal_create_goal, name='goal_create_goal'),
	url(r'^goals/remove', core.views.goal_remove_goal, name='goal_remove_goal'),
	url(r'^goals/join', core.views.goal_join_goal, name='goal_join_goal'),
	url(r'^goals/leave', core.views.goal_leave_goal, name='goal_leave_goal'),
	url(r'^goals/edit', core.views.goal_edit_goal, name='goal_edit_goal'),
	url(r'^goals/log', core.views.goal_edit_goal, name='goal_edit_goal'),
	url(r'^goals/(\d+)/$', core.views.goal_view_goal, name='view_goal'),
	url(r'^goals/(\d+)/edit$', core.views.goal_edit_goal, name='edit_goal'),
    url(r'^goals/(\d+)/log$', core.views.goal_log_progress, name='log_goal'),

	url(r'^users/create', core.views.create_user, name='create_user'),
    url(r'^users/profile', core.views.profile, name='profile'),

	url(r'^users/(\d+)/edit', core.views.edit_user, name='edit_user'),
	url(r'^users/(\d+)/delete', core.views.delete_user, name='delete_user'),
	url(r'^users/(\d+)/$', core.views.view_user, name='view_user'),
	url(r'^users/login/fb', core.views.user_login_fb, name='user_login_fb'),
	url(r'^users/login', core.views.user_login, name='user_login'),

	url(r'^users/logout', core.views.user_logout, name='user_logout'),
	
	#url(r'^users/test/$', core.views.test_user),
	#url(r'^users/test/view', core.views.view_user2),
	#url(r'^users/test/edit', core.views.edit_user2),                       

	url(r'^goals/(\d+)/imageload/$', core.views.goal_image_upload, name ='goal_image_upload'),
	url(r'^users/(\d+)/imageload/$', core.views.user_image_upload, name ='user_image_upload'),
    
    url(r'^goals/goal_add_favorite$', core.views.goal_add_favorite, name ='goal_add_favorite'),
    url(r'^goals/goal_remove_favorite$', core.views.goal_remove_favorite, name ='goal_remove_favorite'),

    url(r'^dashboard', core.views.dashboard, name='dashboard'),                       
    url(r'^confirm', core.views.confirm, name='confirm'),

    

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
