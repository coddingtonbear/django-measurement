from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from measurement import measures

from django_measurement.models import MeasurementField


class MeasurementTestModel(models.Model):
    measurement_distance = MeasurementField(
        measurement=measures.Distance,
        validators=[
            MinValueValidator(measures.Distance(mi=1.0)),
            MaxValueValidator(measures.Distance(mi=3.0))
        ],
        blank=True, null=True,
    )
    measurement_distance_km = MeasurementField(
        measurement=measures.Distance,
        unit_choices=(('km', 'km'),),
        validators=[
            MinValueValidator(measures.Distance(km=1.0)),
            MaxValueValidator(measures.Distance(km=3.0))
        ],
        blank=True, null=True,
    )

    measurement_weight = MeasurementField(
        measurement=measures.Weight,
        validators=[
            MinValueValidator(measures.Weight(kg=1.0)),
            MaxValueValidator(measures.Weight(kg=3.0))
        ],
        blank=True, null=True,
    )

    measurement_speed = MeasurementField(
        measurement=measures.Speed,
        validators=[
            MinValueValidator(measures.Speed(mph=1.0)),
            MaxValueValidator(measures.Speed(mph=3.0))
        ],
        blank=True, null=True,
    )

    measurement_temperature = MeasurementField(
        measurement=measures.Temperature,
        validators=[
            MinValueValidator(measures.Temperature(1.0)),
            MaxValueValidator(measures.Temperature(3.0))
        ],
        blank=True, null=True,
    )

    measurement_speed_mph = MeasurementField(
        measurement=measures.Speed,
        unit_choices=(('mi__hr', 'mph'),),
        validators=[
            MinValueValidator(measures.Speed(mph=1.0)),
            MaxValueValidator(measures.Speed(mph=3.0))
        ],
        blank=True, null=True,
    )

    def __str__(self):
        return self.measurement
