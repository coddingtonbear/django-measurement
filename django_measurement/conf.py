"""Settings for django-measurement."""
from django.conf import settings

from appconf import AppConf

__all__ = ('settings',)


class DjangoMeasurementConf(AppConf):
    """Settings for django-measurement."""

    BIDIMENSIONAL_SEPARATOR = '/'
    """
    For measurement classes subclassing a BidimensionalMeasure, this .
    """

    class Meta:
        prefix = 'measurement'
