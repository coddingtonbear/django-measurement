# -*- coding:utf-8 -*-
from __future__ import (absolute_import, unicode_literals)

import logging

import six
from django.db import models
from django.db.models import Field
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from measurement.base import MeasureBase, BidimensionalMeasure
from measurement import measures
from . import forms
from .utils import get_measurement


logger = logging.getLogger(__name__)


class MeasurementField(six.with_metaclass(models.SubfieldBase, Field)):
    empty_strings_allowed = False
    MEASURE_BASES = (
        BidimensionalMeasure,
        MeasureBase,
    )
    default_error_messages = {
        'invalid_type': _(
            "'%(value)s' (%(type_given)s) value must be of type %(type_wanted)s."
        ),
    }

    def __init__(self, verbose_name=None, name=None, measurement=None,
                 measurement_class=None, unit_choices=None,
                 min_value=None, max_value=None, *args, **kwargs):

        if not measurement and measurement_class:
            measurement = getattr(measures, measurement_class)

        if not measurement:
            raise TypeError('MeasurementField() takes a measurement'
                            ' keyword argument. None given.')

        if not issubclass(measurement, self.MEASURE_BASES):
            raise TypeError('MeasurementField() takes a measurement'
                            ' keyword argument. It has to be a valid MeasureBase'
                            ' subclass.')

        self.measurement = measurement
        self.measurement_class = measurement.__name__
        self.widget_args = {
            'measurement': measurement,
            'unit_choices': unit_choices,
            'max_value': max_value,
            'min_value': min_value
        }

        super(MeasurementField, self).__init__(verbose_name, name, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(MeasurementField, self).deconstruct()
        kwargs['measurement_class'] = self.measurement_class
        return name, path, args, kwargs

    def get_internal_type(self):
        return 'FloatField'

    def get_prep_value(self, value):
        if value is None:
            return None

        elif isinstance(value, self.MEASURE_BASES):
            # sometimes we get sympy.core.numbers.Float, which the
            # database does not understand, so explicitely convert to
            # float

            return float(value.standard)

        else:
            return super(MeasurementField, self).get_prep_value(value)

    def to_python(self, value):
        if value is None:
            return value

        elif isinstance(value, self.measurement):
            return value

        elif isinstance(value, self.MEASURE_BASES):
            raise ValidationError(
                self.error_messages['invalid_type'],
                code='invalid_type',
                params={
                    'value': value,
                    'type_wanted': self.measurement.__name__,
                    'type_given': type(value).__name__
                },
            )

        else:
            value = super(MeasurementField, self).to_python(value)

            original_unit = None

            unit_choices = self.widget_args['unit_choices']
            if unit_choices:
                original_unit = unit_choices[0][0]

            return get_measurement(
                measure=self.measurement,
                value=value,
                original_unit=original_unit,
            )

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.MeasurementFormField}
        defaults.update(kwargs)
        defaults.update(self.widget_args)
        return super(MeasurementField, self).formfield(**defaults)


try:
    from south.modelsinspector import add_introspection_rules

    rules = [
        (
            (MeasurementField,),
            [],
            {
                "measurement_class": ["measurement_class", {}],
            },
        )
    ]

    add_introspection_rules(rules, ["^django_measurement\.fields\.MeasurementField"])
except ImportError:
    pass
