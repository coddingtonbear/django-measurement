from __future__ import unicode_literals

from django.conf.urls import include, url

from django.contrib.admin import site

from . import autocomplete_urls


urlpatterns = [
    url(r'^autocomplete/', include(autocomplete_urls)),

    url(r'^admin/', include(site.urls)),
]
