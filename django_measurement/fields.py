import logging
import re

from django.core.exceptions import ValidationError
from django.db.models import signals
from django.db.models.fields import CharField, Field
from django import forms
from measurement.base import MeasureBase, BidimensionalMeasure

from django_measurement import measure, utils


logger = logging.getLogger(__name__)


class MeasurementFormField(forms.CharField):
    MEASUREMENT_RE = re.compile(r'(?P<value>[0-9.]+) ?(?P<unit>[A-Za-z_]+)')

    def to_python(self, value):
        if not value:
            return None
        match = self.MEASUREMENT_RE.match(value)
        if not match:
            raise ValidationError('%s could not be parsed into a known measurement' % value)
        value, unit = match.groups()
        unit = unit.lower()
        measurement = utils.guess_measurement(value, unit)
        if not match:
            raise ValidationError('%s is not a known unit' % unit)
        return measurement

def get_measurement_parts(value):
    if isinstance(value, measure.UnknownMeasure):
        return value.get_measurement_parts()
    measure_name = '%s(%s)' % (
        value.__class__.__name__,
        value.STANDARD_UNIT
    )
    original_unit = value.unit
    standard_value = value.standard
    return measure_name, original_unit, standard_value

class MeasurementFieldDescriptor(object):
    MEASUREMENT_NAME_RE = re.compile(r'([a-zA-Z0-9]+)(?:\(([a-zA-Z0-9_]+)\))?')

    def __init__(self, field, measurement_field_name, original_unit_field_name, measure_field_name):
        self.field = field
        self.measurement_field_name = measurement_field_name
        self.original_unit_field_name = original_unit_field_name
        self.measure_field_name = measure_field_name

    def _get_measure_by_name(self, measure_name):
        measures = utils.build_measure_list()
        return measures[measure_name]

    def _get_measure_name_and_std_unit(self, measure_string):
        return self.MEASUREMENT_NAME_RE.search(measure_string).groups()

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        measure_name, std_unit = self._get_measure_name_and_std_unit(
            getattr(
                instance, 
                self.measure_field_name
            )
        )
        measurement_value = getattr(
            instance,
            self.measurement_field_name,
        )
        original_unit = getattr(
            instance,
            self.original_unit_field_name,
        )
        try:
            instance_measure = self._get_measure_by_name(measure_name)
            if std_unit and instance_measure.STANDARD_UNIT != std_unit:
                raise ValueError(
                    'Measurement %s base unit %s does not match stored %s' %
                    (
                        measure_name,
                        instance_measure.STANDARD_UNIT,
                        std_unit
                    )
                )
            measurement = utils.get_measurement(
                instance_measure,
                measurement_value,
                instance_measure.STANDARD_UNIT,
                original_unit=original_unit
            )
        except (AttributeError, KeyError, ImportError):
            measurement = measure.UnknownMeasure(
                measure=measure_name,
                original_unit=original_unit,
                value=measurement_value,
            )

        return measurement

    def __set__(self, instance, measurement):
        if instance is None:
            raise AttributeError("Must be accessed via instance")

        measure_name, original_unit, standard_value = get_measurement_parts(
            measurement
        )
        
        setattr(instance, self.measure_field_name, measure_name)
        setattr(instance, self.original_unit_field_name, original_unit)
        setattr(instance, self.measurement_field_name, standard_value)

class MeasurementField(Field):
    def __init__(self, 
            *args,
            **kwargs
        ):
        super(MeasurementField, self).__init__(*args, **kwargs)
        self.original_unit_field_name = '%s_unit'
        self.measure_field_name = '%s_measure'
        self.measurement_field_name = '%s_value'

    def get_original_unit_field_name(self):
        return self.original_unit_field_name % self.name

    def get_measure_field_name(self):
        return self.measure_field_name % self.name

    def get_measurement_field_name(self):
        return self.measurement_field_name % self.name

    def contribute_to_class(self, cls, name):
        self.name = name

        original_unit_field_name = self.get_original_unit_field_name()
        self.original_unit_field = CharField(
            editable=False,
            blank=True,
            default='',
            max_length=50,
        )
        cls.add_to_class(original_unit_field_name, self.original_unit_field)

        measure_field_name = self.get_measure_field_name()
        self.measure_field = CharField(
            editable=False,
            blank=True,
            default='',
            max_length=255,
        )
        cls.add_to_class(measure_field_name, self.measure_field)

        measurement_field_name = self.get_measurement_field_name()
        self.measurement_field = CharField(
            editable=False,
            blank=True,
            default='',
            max_length=50,
        )
        cls.add_to_class(measurement_field_name, self.measurement_field)

        field = MeasurementFieldDescriptor(
            self,
            measurement_field_name=measurement_field_name,
            original_unit_field_name=original_unit_field_name,
            measure_field_name=measure_field_name,
        )

        signals.pre_init.connect(self.instance_pre_init, sender=cls, weak=False)

        setattr(cls, self.name, field)

    def instance_pre_init(self, signal, sender, args, kwargs, **_kwargs):
        if self.name in kwargs:
            value = kwargs.pop(self.name)
            measure_name, original_unit, standard_value = get_measurement_parts(
                value
            )
            kwargs[self.get_measure_field_name()] = measure_name
            kwargs[self.get_original_unit_field_name()] = original_unit
            kwargs[self.get_measurement_field_name()] = standard_value

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_measurement\.fields\.MeasurementField"])
except ImportError:
    pass
