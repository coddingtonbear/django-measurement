from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from measurement import measures

from django_measurement.models import MeasurementField
from tests.custom_measure_base import DegreePerTime, Temperature, Time


class MeasurementTestModel(models.Model):
    measurement_distance = MeasurementField(
        measurement=measures.Distance,
        validators=[
            MinValueValidator(measures.Distance(mi=1.0)),
            MaxValueValidator(measures.Distance(mi=3.0))
        ],
        blank=True, null=True, decimal=True, max_digits=20,
        decimal_places=10
    )

    measurement_distance_km = MeasurementField(
        measurement=measures.Distance,
        unit_choices=(('km', 'km'),),
        validators=[
            MinValueValidator(measures.Distance(km=1.0)),
            MaxValueValidator(measures.Distance(km=3.0))
        ],
        blank=True, null=True, decimal=True, max_digits=20,
        decimal_places=10
    )

    measurement_weight = MeasurementField(
        measurement=measures.Mass,
        validators=[
            MinValueValidator(measures.Mass(kg=1.0)),
            MaxValueValidator(measures.Mass(kg=3.0))
        ],
        blank=True, null=True, decimal=True, max_digits=20,
        decimal_places=10
    )

    measurement_speed = MeasurementField(
        measurement=measures.Speed,
        validators=[
            MinValueValidator(measures.Speed(mph=1.0)),
            MaxValueValidator(measures.Speed(mph=3.0))
        ],
        blank=True, null=True, decimal=True, max_digits=20,
        decimal_places=10
    )

    measurement_temperature = MeasurementField(
        measurement=measures.Temperature,
        validators=[
            MinValueValidator(measures.Temperature(1.0)),
            MaxValueValidator(measures.Temperature(3.0))
        ],
        blank=True, null=True, decimal=True, max_digits=20,
        decimal_places=10
    )

    measurement_temperature2 = MeasurementField(
        measurement_class='Temperature',
        validators=[
            MinValueValidator(measures.Temperature(1.0)),
            MaxValueValidator(measures.Temperature(3.0))
        ],
        blank=True, null=True, decimal=True, max_digits=20,
        decimal_places=10
    )

    measurement_speed_mph = MeasurementField(
        measurement=measures.Speed,
        unit_choices=(('mi__hr', 'mph'),),
        validators=[
            MinValueValidator(measures.Speed(mph=1.0)),
            MaxValueValidator(measures.Speed(mph=3.0))
        ],
        blank=True, null=True, decimal=True, max_digits=20,
        decimal_places=10
    )

    measurement_custom_degree_per_time = MeasurementField(
        measurement=DegreePerTime,
        blank=True, null=True, decimal=True, max_digits=20,
        decimal_places=10
    )

    measurement_custom_temperature = MeasurementField(
        measurement=Temperature,
        blank=True, null=True, decimal=True, max_digits=20,
        decimal_places=10
    )

    measurement_custom_time = MeasurementField(
        measurement=Time,
        blank=True, null=True, decimal=True, max_digits=20,
        decimal_places=10
    )

    def __str__(self):
        return self.measurement
