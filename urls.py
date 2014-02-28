from django.conf.urls.defaults import patterns, include, handler404, handler500, url
from django.conf import settings
from django.http import HttpResponseRedirect

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',lambda x: HttpResponseRedirect('notes/')),
    (r'%s' % settings.ASKBOT_URL, include('askbot.urls')),
    (r'^notes/', include('notes.urls')),
    (r'^admin/', include(admin.site.urls)),
    #(r'^cache/', include('keyedcache.urls')), - broken views disable for now
    (r'^settings/', include('askbot.deps.livesettings.urls')),
    (r'^followit/', include('followit.urls')),
    (r'^robots.txt$', include('robots.urls')),
    url( # TODO: replace with django.conf.urls.static ?
        r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT.replace('\\','/')},
    ),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social',
                             app_name='social'))
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                    url(r'^rosetta/', include('rosetta.urls')),
                )
