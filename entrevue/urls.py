from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from rdv.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'entrevue.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<rdvid>[-A-Za-z0-9_]+)$', RDVView.as_view(), name="rdv_page"),
    url(r'^$', IndexView.as_view(), name="index"),

)
