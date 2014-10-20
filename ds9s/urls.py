from django.conf.urls import patterns, url, include

urlpatterns = patterns('ds9s.views',
	url(r'^/?$', 'viewHomeGalaxy'),
	url(r'^/login/?$','connect'),
	url(r'^/logout/?$','deconnect'),
	url(r'^/newUser/?$','newUser'),
	url(r'^/update/(?P<pk>[0-9]+)/?$','updateUser'),
	url(r'^/information/?$','information'),
	url(r'^/started/?$','gettingStarted'),
	url(r'^/account/?$','myAccount'),
	
	url(r'^/fits/$','viewHomeGalaxy'),
	#url(r'^/fits/search/?$','search'),
	url(r'^/fits/test/?$','displayImage'),
	url(r'^/fits/view/(?P<id>[0-9]+)/?$','viewGalaxy'),
	url(r'^/fits/upload/','newParFile'),
	url(r'^/fits/zoom/(?P<id>[0-9]+)/?$','zoomFile')
)