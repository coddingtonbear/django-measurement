from __future__ import unicode_literals

from django.conf.urls import url

from .views import ProductAutocomplete


urlpatterns = [
    url('product-autocomplete/$', ProductAutocomplete.as_view(), name='product-autocomplete'),
]
