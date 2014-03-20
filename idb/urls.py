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
<<<<<<< HEAD
	url('^yoshio_sakamoto/', 'idb.views.yoshio_sakamoto', name='yoshio_sakamoto'),
        
=======
    url('^crash bandicoot/', 'idb.views.crash bandicoot', name='crash bandicoot')
    url('^nintendo/', 'idb.views.nintendo', name='nintendo'),

>>>>>>> a4eb5fdd121e9d914dd5273cafe9d68673d7c2cb
)
