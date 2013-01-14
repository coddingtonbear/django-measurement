from django.db.models import signals
from django.db.models.fields import CharField, FloatField, CharField

from django_measurement import measure


class MeasurementTypeField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 10)
        kwargs['choices'] = kwargs.get('choices', zip(measure.__all__, measure.__all__))
        super(MeasurementTypeField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'


class MeasurementField(FloatField):
    def get_internal_type(self):
        return 'FloatField'


class OriginalUnitField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 20)
        super(OriginalUnitField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'


class Measurement(object):
    def __init__(self, 
            measurement_field='measurement', 
            measurement_type_field='measurement_type', 
            original_unit_field=None
        ):
        super(Measurement, self).__init__()
        self.measurement_field = measurement_field
        self.measurement_type_field = measurement_type_field
        self.original_unit_field = original_unit_field

    def contribute_to_class(self, cls, name):
        self.name = name
        self.model = cls
        cls._meta.add_virtual_field(self)

        signals.pre_init.connect(self.instance_pre_init, sender=cls, weak=False)

        setattr(cls, name, self)

    def instance_pre_init(self, signal, sender, args, kwargs, **_kwargs):
        if self.name in kwargs:
            value = kwargs.pop(self.name)
            kwargs[self.measurement_field] = getattr(value, value.STANDARD_UNIT)
            kwargs[self.measurement_type_field] = value.__class__.__name__
            if self.original_unit_field:
                kwargs[self.original_unit_field] = value._default_unit

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        type_field = self.model._meta.get_field(self.measurement_type_field)
        measurement_type = getattr(
            measure,
            getattr(instance, self.measurement_type_field)
        )
        value = getattr(
            instance,
            self.measurement_field,
            0
        )
        measurement = measurement_type(
            **{measurement_type.STANDARD_UNIT: value}
        )
        if self.original_unit_field:
            original_unit = getattr(
                instance,
                self.original_unit_field
            )
            measurement._default_unit = original_unit

        return measurement

    def __set__(self, instance, measurement):
        if instance is None:
            raise AttributeError("Must be accessed via instance")

        measurement_type = measurement.__class__.__name__
        value = getattr(measurement, measurement.STANDARD_UNIT, 0)

        setattr(instance, self.measurement_type_field, measurement_type)
        setattr(instance, self.measurement_field, value)
        if self.original_unit_field:
            setattr(instance, self.original_unit_field, measurement._default_unit)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_measurement\.fields\.(MeasurementTypeField|MeasurementField|OriginalUnitField)"])
except ImportError:
    pass
