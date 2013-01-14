from django.db.models import signals
from django.db.models.fields import CharField, DecimalField, CharField

from django_measurement import measure


class MeasurementTypeField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = kwargs.get('choices', zip(measure.__all__, measure.__all__))
        kwargs['max_length'] = kwargs.get('max_length', 10)
        super(MeasurementTypeField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'MeasurementTypeField'


class MeasurementField(DecimalField):
    def get_internal_type(self):
        return 'MeasurementField'


class OriginalUnitField(CharField):
    def get_internal_type(self):
        return 'OriginalUnitField'


class Measurement(object):
    def __init__(self, 
            measurement_field='measurement', 
            measurement_type_field='measurement_type', 
            original_unit_field=None
        ):
        super(MeasurementField, self).__init__()
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
        measure = measurement_type(
            **{measurement_type.STANDARD_UNIT: value}
        )
        if self.original_unit_field:
            original_unit = getattr(
                instance,
                self.original_unit_field
            )
            measure._default_unit = original_unit

        return measure

    def __set__(self, instance, measure):
        if instance is None:
            raise AttributeError("Must be accessed via instance")

        measurement_type = measure.__class__.__name__
        value = getattr(measure, measure.STANDARD_UNIT, 0)

        setattr(instance, self.measurement_type_field, measurement_type)
        setattr(instance, self.measurement_field, value)
        if self.original_unit_field:
            setattr(instance, self.original_unit_field, measure._default_unit)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_measurement\.fields\.(MeasurementTypeField|MeasurementField|OriginalUnitField)"])
except ImportError:
    pass
