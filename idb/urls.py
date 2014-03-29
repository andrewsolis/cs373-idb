from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'idb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', 'idb.views.home', name='home'),
    url(r'^$', 'idb.views.home', name='home'),
    url(r'^metroid/', 'idb.views.metroid', name='metroid'),
	url(r'^yoshio_sakamoto/', 'idb.views.yoshio_sakamoto', name='yoshio_sakamoto'),
	url(r'^naoto_oshima/', 'idb.views.naoto_oshima', name='naoto_oshima'),
	url(r'^andy_gavin/', 'idb.views.andy_gavin', name='andy_gavin'),
    url(r'^crash_bandicoot/', 'idb.views.crash_bandicoot', name='crash_bandicoot'),
    url(r'^nintendo/', 'idb.views.nintendo', name='nintendo'),
    url(r'^sonic/', 'idb.views.sonic', name='sonic'),
    url(r'^games_index/', 'idb.views.games_index', name='games_index'),
    url(r'^people_index/', 'idb.views.people_index', name='people_index'),
    url(r'^companies_index/', 'idb.views.companies_index', name='companies_index'),
    url(r'^sega/', 'idb.views.sega', name='sega'),
    url(r'^naughtydog/', 'idb.views.naughtydog', name='naughtydog'),

    url(r'^games/', 'idb.views.games', name='games_index'),
)
