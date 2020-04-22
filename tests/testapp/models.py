from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django_measurement.models import MeasurementField

from measurement import measures


class MeasurementTestModel(models.Model):
    measurement_distance = MeasurementField(
        measure=measures.Distance,
        validators=[
            MinValueValidator(measures.Distance(mi=1)),
            MaxValueValidator(measures.Distance(mi=3)),
        ],
        blank=True,
        null=True,
        max_digits=28,
        decimal_places=3,
    )

    measurement_mass = MeasurementField(
        measure=measures.Mass,
        validators=[
            MinValueValidator(measures.Mass(kg=1)),
            MaxValueValidator(measures.Mass(kg=3)),
        ],
        blank=True,
        null=True,
        max_digits=28,
        decimal_places=3,
    )

    measurement_speed = MeasurementField(
        measure=measures.Speed,
        validators=[
            MinValueValidator(measures.Speed(mph=1)),
            MaxValueValidator(measures.Speed(mph=3)),
        ],
        blank=True,
        null=True,
        max_digits=28,
        decimal_places=3,
    )

    measurement_temperature = MeasurementField(
        measure=measures.Temperature,
        validators=[
            MinValueValidator(measures.Temperature(celsius=1)),
            MaxValueValidator(measures.Temperature(celsius=3)),
        ],
        blank=True,
        null=True,
        max_digits=28,
        decimal_places=3,
    )

    measurement_temperature2 = MeasurementField(
        measure="Temperature",
        validators=[
            MinValueValidator(measures.Temperature(celsius=1)),
            MaxValueValidator(measures.Temperature(celsius=3)),
        ],
        blank=True,
        null=True,
        max_digits=28,
        decimal_places=3,
    )

    measurement_speed_mph = MeasurementField(
        measure=measures.Speed,
        validators=[
            MinValueValidator(measures.Speed(mph=1)),
            MaxValueValidator(measures.Speed(mph=3)),
        ],
        blank=True,
        null=True,
        max_digits=28,
        decimal_places=3,
    )

    measurement_custom_degree_per_time = MeasurementField(
        measure=measures.VolumetricFlowRate,
        blank=True,
        null=True,
        max_digits=28,
        decimal_places=3,
    )

    measurement_custom_temperature = MeasurementField(
        measure=measures.Temperature,
        blank=True,
        null=True,
        max_digits=28,
        decimal_places=3,
    )

    measurement_custom_time = MeasurementField(
        measure=measures.Time, blank=True, null=True, max_digits=28, decimal_places=3,
    )
