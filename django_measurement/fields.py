from django.db.models.fields import CharField, FloatField, CharField

from django_measurement import measure

class MeasurementFieldDescriptor(object):
    def __init__(self, field, measurement_field_name, original_unit_field_name, measure_field_name):
        self.field = field
        self.measurement_field_name = measurement_field_name
        self.original_unit_field_name = original_unit_field_name
        self.measure_field_name = measure_field_name

    def _get_measure(self, instance):
        return getattr(
            measure,
            getattr(instance, self.measure_field_name)
        )

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

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

        return measurement

    def __set__(self, instance, measurement):
        if instance is None:
            raise AttributeError("Must be accessed via instance")
        
        measurement_measure = measurement.__class__.__name__
        setattr(instance, self.measure_field_name, measurement_measure)
        setattr(instance, self.original_unit_field_name, measurement._default_unit)
        setattr(instance, self.measurement_field_name, getattr(measurement, measurement.STANDARD_UNIT, 0))

class MeasurementField(FloatField):
    def __init__(self, 
            *args,
            **kwargs
        ):
        super(MeasurementField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.name = name

        original_unit_field_name = '%s_unit' % self.name
        self.original_unit_field = CharField(
            editable=False,
            blank=True,
            default='',
            max_length=50,
        )
        cls.add_to_class(original_unit_field_name, self.original_unit_field)

        measure_field_name = '%s_measure' % self.name
        self.measure_field = CharField(
            editable=False,
            blank=True,
            default='',
            max_length=255,
        )
        cls.add_to_class(measure_field_name, self.measure_field)

        measurement_field_name = '%s_value' % self.name
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

        setattr(cls, self.name, field)

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        return self.instance_class(instance, self)

    def __set__(self, instance, value):
        if not isinstance(value, measure.MeasureBase):
            raise TypeError('')


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_measurement\.fields\.(MeasuremeField|MeasurementField|OriginalUnitField)"])
except ImportError:
    pass
