from django.conf.urls import patterns, url, include
from ds9s.views import ViewHome, DeleteUser, ViewHomeFits

urlpatterns = patterns('ds9s.views',
	#url(r'^/?$', ViewHome.as_view(), name="ds9s_home"),
	url(r'^/?$', ViewHomeFits.as_view(), name='ds9s_homeFits'),
	url(r'^/view/(?P<id>[0-9]+)','focus'),
	url(r'^/login/?$','connect'),
	url(r'^/logout/?$','deconnect'),
	url(r'^/newUser/?$','newUser'),
	url(r'^/update/(?P<pk>[0-9]+)/?$','updateUser'),
	url(r'^/informations/?$','informations'),
	url(r'^/started/?$','gettingStarted'),
	url(r'^/delete/(?P<pk>[0-9]+)/?$',DeleteUser.as_view(), name="delete_user"),
	url(r'^/account/?$','myAccount'),
	
	url(r'^/fits/$',ViewHomeFits.as_view(), name='ds9s_homeFits'),
	url(r'^/fits/test/?$','test'),
	url(r'^/fits/view/(?P<id>[0-9]+)/?$','viewGalaxy'),
	url(r'^/fits/upload/','newParFile')
)