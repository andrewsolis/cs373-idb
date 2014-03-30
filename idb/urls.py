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

# missing some intersections
    url(r'^games/(\d+)/people/', 'idb.views.games_people', name='games_people'),
    url(r'^games/(\d+)/companies/', 'idb.views.games_companies', name='games_companies'),
    url(r'^api/games/(\d+)/people/', 'idb.api.views.games_people', name='api_games_people'),
    url(r'^api/games/(\d+)/companies/', 'idb.api.views.games_companies', name='api_games_companies'),


    url(r'^games/(\d+)/', 'idb.views.games_id', name='games_id'),
    url(r'^people/(\d+)/', 'idb.views.people_id', name='people_id'),
    url(r'^companies/(\d+)/', 'idb.views.companies_id', name='companies_id'),
    url(r'^api/games/(\d+)/', 'idb.api.views.games_id', name='api_games_id'),
    url(r'^api/people/(\d+)/', 'idb.api.views.people_id', name='api_people_id'),
    url(r'^api/companies/(\d+)/', 'idb.api.views.companies_id', name='api_companies_id'),

    url(r'^games/', 'idb.views.games', name='games'),
    url(r'^people/', 'idb.views.people', name='people'),
    url(r'^companies/', 'idb.views.companies', name='companies'),
    url(r'^api/games/', 'idb.api.views.games', name='api_games'),
    url(r'^api/people/', 'idb.api.views.people', name='api_people'),
    url(r'^api/companies/', 'idb.api.views.companies', name='api_comanies'),
)
