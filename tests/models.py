from django.db import models
from django_measurement import fields
from measurement import measures


class MeasurementTestModel(models.Model):
    measurement_distance = fields.MeasurementField(
        measurement=measures.Distance,
        max_value=3.0, min_value=1.0,
        blank=True, null=True,
    )
    measurement_distance_km = fields.MeasurementField(
        measurement=measures.Distance,
        unit_choices=(('km', 'km'),),
        max_value=3.0, min_value=1.0,
        blank=True, null=True,
    )

    measurement_weight = fields.MeasurementField(
        measurement=measures.Weight,
        max_value=3.0, min_value=1.0,
        blank=True, null=True,
    )

    measurement_speed = fields.MeasurementField(
        measurement=measures.Speed,
        max_value=3.0, min_value=1.0,
        blank=True, null=True,
    )

    measurement_temperature = fields.MeasurementField(
        measurement=measures.Temperature,
        max_value=3.0, min_value=1.0,
        blank=True, null=True,
    )

    measurement_speed_mph = fields.MeasurementField(
        measurement=measures.Speed,
        unit_choices=(('mi__hr', 'mph'),),
        max_value=3.0, min_value=1.0,
        blank=True, null=True,
    )

    def __unicode__(self):
        return self.measurement
