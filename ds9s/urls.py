from django.conf.urls import patterns, url

urlpatterns = patterns('ds9s.views',
	url(r'^/?$', 'home'),
	url(r'^/date$','tpl'),
	url(r'^/add/(?P<num1>[0-9]+)/(?P<num2>[0-9]+)/$','addition'),
	url(r'^/view/(?P<id>[0-9]+)','focus'),
	url(r'^/login/?$','login'),
	url(r'^/newUser/?$','newUser')
)