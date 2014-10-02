from django.conf.urls import patterns, url, include
from ds9s.views import ViewHome, DeleteUser

urlpatterns = patterns('ds9s.views',
	url(r'^/?$', ViewHome.as_view(), name="ds9s_home"),
	url(r'^/date$','tpl'),
	url(r'^/add/(?P<num1>[0-9]+)/(?P<num2>[0-9]+)/$','addition'),
	url(r'^/view/(?P<id>[0-9]+)','focus'),
	url(r'^/login/?$','connect'),
	url(r'^/logout/?$','deconnect'),
	url(r'^/newUser/?$','newUser'),
	url(r'^/update/(?P<pk>[0-9]+)/?$','updateUser'),
	url(r'^/delete/(?P<pk>[0-9]+)/?$',DeleteUser.as_view(), name="delete_user")
)