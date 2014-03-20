from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'idb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^home/', 'idb.views.home', name='home'),
    url('^$', 'idb.views.home', name='home'),
    url('^metroid/', 'idb.views.metroid', name='metroid'),
	url('^yoshio_sakamoto/', 'idb.views.yoshio_sakamoto', name='yoshio_sakamoto'),
    url('^crash_bandicoot/', 'idb.views.crash_bandicoot', name='crash_bandicoot'),
    url('^nintendo/', 'idb.views.nintendo', name='nintendo'),
    url('^sonic/', 'idb.views.sonic', name='sonic'),
    url('^games_index/', 'idb.views.games_index', name='games_index'),
    url('^people_index/', 'idb.views.people_index', name='people_index'),
    url('^companies_index/', 'idb.views.companies_index', name='companies_index'),

)
