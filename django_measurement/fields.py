from django.conf import settings
from django.db.models import signals
from django.db.models.fields import CharField, FloatField, CharField

from django_measurement import measure

MEASURE_OVERRIDES = getattr(settings, 'MEASURE_OVERRIDES', {})

def get_measurement_parts(value):
    measure_name = value.__class__.__name__
    original_unit = value._default_unit
    standard_value = getattr(value, value.STANDARD_UNIT)
    return measure_name, original_unit, standard_value

class MeasurementFieldDescriptor(object):
    def __init__(self, field, measurement_field_name, original_unit_field_name, measure_field_name):
        self.field = field
        self.measurement_field_name = measurement_field_name
        self.original_unit_field_name = original_unit_field_name
        self.measure_field_name = measure_field_name

    def _get_class_by_path(self, path):
        mod = __import__('.'.join(path.split('.')[:-1]))
        components = path.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def _get_measure(self, instance):
        measure_name = getattr(instance, self.measure_field_name)
        if measure_name in MEASURE_OVERRIDES:
            return self._get_class_by_path(
                MEASURE_OVERRIDES[measure_name]
            )
        return getattr(
            measure,
            measure_name
        )

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        try:
            instance_measure = self._get_measure(instance)
            measurement_value = getattr(
                instance,
                self.measurement_field_name,
            )
            measurement = instance_measure(
                **{instance_measure.STANDARD_UNIT: measurement_value}
            )
            original_unit = getattr(
                instance,
                self.original_unit_field_name,
            )
            measurement._default_unit = original_unit
        except (AttributeError, ValueError):
            return None

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

class MeasurementField(FloatField):
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
