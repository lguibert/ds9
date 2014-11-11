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
	url(r'^/fits/test/?$','test'),
	url(r'^/fits/scaling/(?P<val>[0-9]+)/(?P<color>[a-zA-Z]{4,8}\-[0-9]{1,2})/?$','scaling'),
	url(r'^/fits/wavelenghing/(?P<redshift>[0-9\.]+)/(?P<mode>[a-z]+)/?$','wavelenghing'),
	url(r'^/fits/referencing/(?P<redshift>[0-9\.]+)/(?P<mode>[a-z]+)/?$','referencing'),
	url(r'^/fits/view/(?P<uid>[0-9]+)/?$','viewGalaxy'),
	url(r'^/fits/view/?$','viewGalaxy'),
	url(r'^/fits/saveReview/(?P<id>[0-9]+)/(?P<uniq_id>[0-9]+)/?$','saveUserReview'),
	url(r'^/fits/upload/','newParFile'),
	#url(r'^/fits/zoom/(?P<id>[0-9]+)/?$','zoomFile')
)