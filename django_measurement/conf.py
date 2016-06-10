# -*- coding: utf-8 -*-
"""Settings for django-measurement."""
from __future__ import absolute_import, unicode_literals

from appconf import AppConf
from django.conf import settings

__all__ = ('settings', 'DjangoMeasurementConf')


class DjangoMeasurementConf(AppConf):
    """Settings for django-measurement."""

    BIDIMENSIONAL_SEPARATOR = '/'
    """
    For measurement classes subclassing a BidimensionalMeasure, this .
    """

    class Meta:
        prefix = 'measurement'
