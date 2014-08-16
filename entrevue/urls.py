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
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^$', CreatedView.as_view(), name="created"),
    #    url(r'^(?P<cid>[-A-Za-z0-9_]+)$', 'rdv.views.rdv_page', name="rdv_page"),

)
