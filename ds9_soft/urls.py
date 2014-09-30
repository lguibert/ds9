from django.conf.urls import patterns, url

urlpatterns = patterns('ds9_soft.views',
	url(r'^$', 'home'),
	url(r'^/date$','tpl'),
	url(r'^/add/(?P<num1>[0-9]+)/(?P<num2>[0-9]+)/$','addition'),
)
