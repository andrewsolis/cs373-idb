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

    # missing some intersections
    url(r'^games/(\d+)/people/', 'idb.views.games_people', name='games_people'),
    url(r'^games/(\d+)/companies/', 'idb.views.games_companies', name='games_companies'),
    url(r'^people/(\d+)/games/', 'idb.views.people_games', name='people_games'),
    url(r'^people/(\d+)/companies/', 'idb.views.people_companies', name='people_companies'),
    url(r'^companies/(\d+)/games/', 'idb.views.companies_games', name='companies_games'),
    url(r'^companies/(\d+)/people/', 'idb.views.companies_people', name='companies_people'),
    url(r'^api/games/(\d+)/people/', 'idb.api.views.api_games_people', name='api_games_people'),
    url(r'^api/games/(\d+)/companies/', 'idb.api.views.api_games_companies', name='api_games_companies'),
    url(r'^api/people/(\d+)/games/', 'idb.api.views.api_people_games', name='api_people_games'),
    url(r'^api/people/(\d+)/companies/', 'idb.api.views.api_people_companies', name='api_people_companies'),
    url(r'^api/companies/(\d+)/games/', 'idb.api.views.api_companies_games', name='api_companies_games'),
    url(r'^api/companies/(\d+)/people/', 'idb.api.views.api_companies_people', name='api_companies_people'),

    url(r'^games/(\d+)', 'idb.views.games_id', name='games_id'),
    url(r'^people/(\d+)', 'idb.views.people_id', name='people_id'),
    url(r'^companies/(\d+)', 'idb.views.companies_id', name='companies_id'),
    url(r'^api/games/(\d+)/', 'idb.api.views.api_games_id', name='api_games_id'),
    url(r'^api/people/(\d+)/', 'idb.api.views.api_people_id', name='api_people_id'),
    url(r'^api/companies/(\d+)/', 'idb.api.views.api_companies_id', name='api_companies_id'),

    url(r'^games/', 'idb.views.games', name='games'),
    url(r'^people/', 'idb.views.people', name='people'),
    url(r'^companies/', 'idb.views.companies', name='companies'),
    url(r'^api/games/', 'idb.api.views.api_games', name='api_games'),
    url(r'^api/people/', 'idb.api.views.api_people', name='api_people'),
    url(r'^api/companies/', 'idb.api.views.api_companies', name='api_comanies'),
)
