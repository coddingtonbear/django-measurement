from django.db import models
from measurement import measures

from django_measurement.models import MeasurementField


class MeasurementTestModel(models.Model):
    measurement_distance = MeasurementField(
        measurement=measures.Distance,
        max_value=3.0, min_value=1.0,
        blank=True, null=True,
    )
    measurement_distance_km = MeasurementField(
        measurement=measures.Distance,
        unit_choices=(('km', 'km'),),
        max_value=3.0, min_value=1.0,
        blank=True, null=True,
    )

    measurement_weight = MeasurementField(
        measurement=measures.Weight,
        max_value=3.0, min_value=1.0,
        blank=True, null=True,
    )

    measurement_speed = MeasurementField(
        measurement=measures.Speed,
        max_value=3.0, min_value=1.0,
        blank=True, null=True,
    )

    measurement_temperature = MeasurementField(
        measurement=measures.Temperature,
        max_value=3.0, min_value=1.0,
        blank=True, null=True,
    )

    measurement_speed_mph = MeasurementField(
        measurement=measures.Speed,
        unit_choices=(('mi__hr', 'mph'),),
        max_value=3.0, min_value=1.0,
        blank=True, null=True,
    )

    def __unicode__(self):
        return self.measurement
