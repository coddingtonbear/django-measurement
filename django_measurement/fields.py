# -*- coding:utf-8 -*-
from __future__ import (absolute_import, unicode_literals)

import logging

import re
from warnings import warn
from django.db.models import signals, Manager
from django.db.models.query import QuerySet
from django.db.models import CharField, Field, FloatField, NOT_PROVIDED
from measurement.base import MeasureBase
from . import measure, utils, forms


logger = logging.getLogger(__name__)


class OriginalUnitField(CharField):
    pass


class MeasureNameField(CharField):
    pass


class MeasurementValueField(FloatField):
    pass


def get_measurement_parts(value):
    if isinstance(value, measure.UnknownMeasure):
        return value.get_measurement_parts()
    measure_name = '%s(%s)' % (value.__class__.__name__, value.STANDARD_UNIT)
    original_unit = value.unit
    standard_value = value.standard
    return measure_name, original_unit, standard_value


class MeasurementFieldDescriptor(object):
    MEASUREMENT_NAME_RE = re.compile(r'([a-zA-Z0-9]+)(?:\(([a-zA-Z0-9_]+)\))?')

    def __init__(self, field, measurement_field_name, original_unit_field_name,
                 measure_field_name):
        self.field = field
        self.measurement_field_name = measurement_field_name
        self.original_unit_field_name = original_unit_field_name
        self.measure_field_name = measure_field_name

    def _get_measure_by_name(self, measure_name):
        measures = utils.build_measure_list()
        return measures[measure_name]

    def _get_measure_name_and_std_unit(self, measure_string):
        return self.MEASUREMENT_NAME_RE.search(measure_string).groups()

    def __get__(self, obj, type=None):
        if obj is None:
            return self

        measure_packed = getattr(obj, self.measure_field_name)
        if measure_packed:
            measure_name, std_unit = self._get_measure_name_and_std_unit(measure_packed)
        else:
            measure_name = ''
            std_unit = ''
        measurement_value = getattr(obj, self.measurement_field_name, )
        original_unit = getattr(obj, self.original_unit_field_name)
        if not measure_name or not original_unit:
            return obj.__dict__[self.field.name]

        try:
            instance_measure = self._get_measure_by_name(measure_name)
            if std_unit and instance_measure.STANDARD_UNIT != std_unit:
                raise ValueError(
                    'Measurement %s base unit %s does not match stored %s' % (
                        measure_name,
                        instance_measure.STANDARD_UNIT,
                        std_unit
                    ))
            obj.__dict__[self.field.name] = utils.get_measurement(
                instance_measure,
                measurement_value,
                instance_measure.STANDARD_UNIT,
                original_unit=original_unit
            )
        except (AttributeError, KeyError, ImportError):
            obj.__dict__[self.field.name] = measure.UnknownMeasure(
                measure=measure_name,
                original_unit=original_unit,
                value=measurement_value,
            )

        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        if obj is None:
            raise AttributeError("Must be accessed via instance")

        if value:
            measure, original_unit, standard_value = get_measurement_parts(value)
        else:
            measure = ''
            original_unit = ''
            standard_value = 0

        setattr(obj, self.measure_field_name, measure)
        setattr(obj, self.original_unit_field_name, original_unit)
        setattr(obj, self.measurement_field_name, standard_value)


class MeasurementField(Field):
    """
    A Django db field for  python measurement library objects.
    """
    original_unit_field_name = '%s_unit'
    measure_field_name = '%s_measure'
    measurement_field_name = '%s_value'

    def __init__(self, verbose_name=None, name=None,
                 measurement=None, choices=None,
                 max_value=None, min_value=None, *args, **kwargs):
        if not measurement:
            warn(DeprecationWarning,
                 "measurement should be set to use django's ModelForm.")

        self.widget_args = {
            'measurement': measurement,
            'choices': choices,
            'max_value': max_value,
            'min_value': min_value
        }
        super(MeasurementField, self).__init__(*args, **kwargs)

    def get_original_unit_field_name(self):
        return self.original_unit_field_name % self.name

    def get_measure_field_name(self):
        return self.measure_field_name % self.name

    def get_measurement_field_name(self):
        return self.measurement_field_name % self.name

    def contribute_to_class(self, cls, name, **kwargs):
        self.name = name

        if self.default is not NOT_PROVIDED:
            parts = get_measurement_parts(self.default)
            default_name, default_unit, default_value = parts
        else:
            default_name, default_unit, default_value = '', '', 0.0

        original_unit_field_name = self.get_original_unit_field_name()
        self.original_unit_field = OriginalUnitField(
            blank=True,
            default=default_unit,
            max_length=50,
            editable=False
        )
        cls.add_to_class(original_unit_field_name, self.original_unit_field)

        measure_field_name = self.get_measure_field_name()
        self.measure_field = MeasureNameField(
            blank=True,
            default=default_name,
            max_length=255,
            editable=False
        )
        cls.add_to_class(measure_field_name, self.measure_field)

        measurement_field_name = self.get_measurement_field_name()
        self.measurement_field = MeasurementValueField(
            blank=True,
            default=default_value,
            max_length=50,
            editable=False
        )
        cls.add_to_class(measurement_field_name, self.measurement_field)

        field = MeasurementFieldDescriptor(
            self,
            measurement_field_name=measurement_field_name,
            original_unit_field_name=original_unit_field_name,
            measure_field_name=measure_field_name,
        )

        signals.pre_init.connect(self.instance_pre_init, sender=cls, weak=False)

        super(MeasurementField, self).contribute_to_class(cls, name, virtual_only=True)
        setattr(cls, self.name, field)

        class MeasurementManager(Manager):
            use_for_related_fields = True

            def get_query_set(self):
                return MeasurementQuerySet(model=cls)

        cls.add_to_class('objects', MeasurementManager())

    def instance_pre_init(self, signal, sender, args, kwargs, **_kwargs):
        if self.name in kwargs:
            value = kwargs.pop(self.name)
            measure_name, original_unit, standard_value = get_measurement_parts(
                value
            )
            kwargs[self.get_measure_field_name()] = measure_name
            kwargs[self.get_original_unit_field_name()] = original_unit
            kwargs[self.get_measurement_field_name()] = standard_value

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.MeasurementFormField}
        defaults.update(kwargs)
        defaults.update(self.widget_args)
        return super(MeasurementField, self).formfield(**defaults)


class MeasurementQuerySet(QuerySet):
    def filter(self, *args, **kwargs):
        kwargs = self._fix_fields(kwargs)
        return super(MeasurementQuerySet, self).filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        kwargs = self._fix_fields(kwargs)
        return super(MeasurementQuerySet, self).exclude(*args, **kwargs)

    def get(self, *args, **kwargs):
        kwargs = self._fix_fields(kwargs)
        return super(MeasurementQuerySet, self).get(*args, **kwargs)

    def _fix_fields(self, kwargs):
        copy = kwargs.copy()
        for key, val in kwargs.items():
            if issubclass(val.__class__, MeasureBase):
                name, unit, value = get_measurement_parts(val)
                copy[key + '_measure'] = name
                copy[key + '_unit'] = unit
                copy[key + '_value'] = value
                del copy[key]
        return copy


try:
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([], ["^django_measurement\.fields\.MeasurementField"])
    add_introspection_rules([], ["^django_measurement\.fields\.OriginalUnitField"])
    add_introspection_rules([], ["^django_measurement\.fields\.MeasureNameField"])
    add_introspection_rules([], ["^django_measurement\.fields\.MeasurementValueField"])
except ImportError:
    pass
