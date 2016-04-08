# -*- coding: utf-8 -*-

from sympy import S, Symbol
from measurement.base import BidimensionalMeasure, MeasureBase

__all__ = (
    'Temperature',
    'Time',
    'DegreePerTime',
)


class Temperature(MeasureBase):
    SU = Symbol('kelvin')
    STANDARD_UNIT = 'k'
    UNITS = {
        'c': SU - S(273.15),
        'f': (SU - S(273.15)) * S('9/5') + 32,
        'k': 1.0
    }
    LABELS = {
        'c': u'°C',
        'f': u'°F',
        'k': u'°K',
    }


class Time(MeasureBase):
    UNITS = {
        's': 3600.0,
        'h': 1.0,
    }
    SI_UNITS = ['s']


class DegreePerTime(BidimensionalMeasure):
    PRIMARY_DIMENSION = Temperature
    REFERENCE_DIMENSION = Time
