from django.conf.urls import patterns, url, include

urlpatterns = patterns('ds9s.views',
	url(r'^/?$', 'viewHomeGalaxy'),
	url(r'^/login/?$','connect'),
	url(r'^/logout/?$','deconnect'),
	url(r'^/newUser/?$','newUser'),
	url(r'^/account/update/?$','updateUser'),
	url(r'^/information/?$','information'),
	url(r'^/started/?$','gettingStarted'),
	url(r'^/account/?$','myAccount'),
	
	#url(r'^/$','viewHomeGalaxy'),
	#url(r'^/search/?$','search'),
	url(r'^/test/?$','test'),
	url(r'^/scaling/(?P<val>[0-9]+)/(?P<color>[a-zA-Z]{4,8}\-[0-9]{1,2})/?$','scaling'),
	url(r'^/wavelenghing/(?P<redshift>[0-9\.]+)/(?P<mode>[a-z]+)/(?P<color>[a-zA-Z]{4,8}\-[0-9]{1,2})/?$','wavelenghing'),
	url(r'^/referencing/(?P<redshift>[0-9\.]+)/(?P<mode>[a-z]+)/?$','referencing'),
	url(r'^/coloring/(?P<val>[0-9]+)/(?P<redshift>[0-9\.]+)/(?P<color>[a-zA-Z]{4,8}\-[0-9]{1,2})/?$','coloring'),
	url(r'^/oneLining/?$','oneLining'),
	#url(r'^/view/(?P<uid>[0-9]+)/?$','viewGalaxy'),
	url(r'^/view/(?P<name>[0-9]+_[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/?$','viewGalaxy'),
	url(r'^/view/?$','viewGalaxy'),
	url(r'^/saveReview/(?P<id>[0-9]+)/(?P<uniq_name>[0-9]+_[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/(?P<next_uniq_name>[0-9]+_[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/?$','saveUserReview'),
	url(r'^/saveReview/(?P<id>[0-9]+)/(?P<uniq_name>[0-9]+_[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/(?P<next_uniq_name>None)/?$','saveUserReview'),
	url(r'^/updateReview/(?P<rev_id>[0-9]+)/?$','updateUserReview'),
	url(r'^/upload/','newParFile'),
	#url(r'^/zoom/(?P<id>[0-9]+)/?$','zoomFile')

	url(r'^/account/reviews/?$','getReviewUser'),
	url(r'^/reviews/?$','viewAllReviews'),
	url(r'^/reviews/(?P<uniq_name>[0-9]+_[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12})/?$','viewReviewAnalysis'),
)