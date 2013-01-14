from django.db.models import signals, SubfieldBase
from django.db.models.fields import CharField, FloatField, CharField

from django_measurement import measure


class MeasureField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 10)
        kwargs['choices'] = kwargs.get('choices', zip(measure.__all__, measure.__all__))
        super(MeasureField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'


class OriginalUnitField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 20)
        super(OriginalUnitField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'


class MeasurementFieldDescriptor(object):
    def __init__(self, field):
        self.field = field

    def _get_measurement_type(self, instance):
        if self.field.measure_field:
            return getattr(
                measure,
                getattr(instance, self.field.measure_field)
            )
        return self.field.measure

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        instance_measure = self._get_measurement_type(instance)
        measurement_value = getattr(
            instance,
            self.field.attname
        )
        measurement = instance_measure(
            **{instance_measure.STANDARD_UNIT: measurement_value}
        )
        if self.field.original_unit_field:
            original_unit = getattr(
                instance,
                self.field.original_unit_field
            )
            measurement._default_unit = original_unit

        return measurement

    def __set__(self, instance, measurement):
        if instance is None:
            raise AttributeError("Must be accessed via instance")
        
        if self.field.measure:
            if not isinstance(self.field.measure, measurement):
                raise ValueError("Accepts only instances of type %s" % self.field.measure)
        else:
            measurement_measure = measurement.__class__.__name__
            setattr(instance, self.field.measure_field, measurement_measure)

        if self.field.original_unit_field:
            setattr(instance, self.field.original_unit_field, measurement._default_unit)

        setattr(instance, self.field.attname, getattr(measurement, measurement.STANDARD_UNIT, 0))

class MeasurementField(FloatField):
    def __init__(self, 
            measure=None,
            measure_field=None, 
            original_unit_field=None,
            *args,
            **kwargs
        ):
        super(MeasurementField, self).__init__(*args, **kwargs)
        self.measure_field = measure_field
        self.measure = measure
        if not self.measure_field and not self.measure:
            raise AttributeError('You must specify either measure_field or measure')
        self.original_unit_field = original_unit_field

    def get_attname(self):
        return '%s_value' % self.name

    def get_attname_column(self):
        return self.get_attname(), self.name

    def contribute_to_class(self, cls, name):
        super(MeasurementField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, MeasurementFieldDescriptor(self))

    def get_prep_value(self, value):
        return getattr(value, value.STANDARD_UNIT, 0)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_measurement\.fields\.(MeasuremeField|MeasurementField|OriginalUnitField)"])
except ImportError:
    pass
