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
	
	#url(r'^/$','viewHomeGalaxy'),
	#url(r'^/search/?$','search'),
	url(r'^/test/?$','test'),
	url(r'^/scaling/(?P<val>[0-9]+)/(?P<color>[a-zA-Z]{4,8}\-[0-9]{1,2})/?$','scaling'),
	url(r'^/wavelenghing/(?P<redshift>[0-9\.]+)/(?P<mode>[a-z]+)/?$','wavelenghing'),
	url(r'^/referencing/(?P<redshift>[0-9\.]+)/(?P<mode>[a-z]+)/?$','referencing'),
	#url(r'^/view/(?P<uid>[0-9]+)/?$','viewGalaxy'),
	url(r'^/view/(?P<name>[0-9]+_[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/?$','viewGalaxy'),
	url(r'^/view/?$','viewGalaxy'),
	url(r'^/saveReview/(?P<id>[0-9]+)/(?P<uniq_name>[0-9]+_[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/(?P<next_uniq_name>[0-9]+_[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/?$','saveUserReview'),
	url(r'^/saveReview/(?P<id>[0-9]+)/(?P<uniq_name>[0-9]+_[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/(?P<next_uniq_name>None)/?$','saveUserReview'),
	url(r'^/updateReview/(?P<rev_id>[0-9]+)/?$','updateUserReview'),
	url(r'^/upload/','newParFile'),
	#url(r'^/zoom/(?P<id>[0-9]+)/?$','zoomFile')

	url(r'^/account/reviews/?$','getReviewUser'),
)