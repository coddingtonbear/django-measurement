# -*- coding:utf-8 -*-
from __future__ import (absolute_import, unicode_literals)

from measurement.utils import total_ordering
from measurement.measures import *  # NOQA


@total_ordering
class UnknownMeasure(object):
    def __init__(self, measure, original_unit, value):
        self.measure = measure
        self.original_unit = original_unit
        self.value = value

    def __getattr__(self, name):
        raise AttributeError(
            'UnknownMeasures cannot be convered to other units.'
        )

    def get_measurement_parts(self):
        return self.measure, self.original_unit, self.value

    def __eq__(self, other):
        if isinstance(other, UnknownMeasure):
            if self.measure == other.measure:
                if self.value == other.value:
                    return True
        return False

    def __lt__(self, other):
        if isinstance(other, UnknownMeasure):
            if self.measure == other.measure:
                if self.value < other.value:
                    return True
                return False
        return NotImplemented

    def __repr__(self):
        return '%s(?=%s)' % (self.measure, self.value)

    def __str__(self):
        return '%s ? (%s)' % (self.value, self.measure)
