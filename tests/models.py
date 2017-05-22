from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible

from measurement import measures

from django_measurement.models import MeasurementField


@python_2_unicode_compatible
class Product(models.Model):
    """
    Product model.
    """
    name = models.CharField(
        _('name'),
        help_text=_('Name of the product.'),
        max_length=255,
        blank=False,
        null=False
    )
    weight = MeasurementField(
        _('gross weight'),
        measurement=measures.Weight,
        unit_choices=(('kg', 'kg'),),
    )
    volume = MeasurementField(
        _('volume'),
        measurement=measures.Volume,
        unit_choices=(('cubic_meter', _('cubic meter')),),
    )
    width = MeasurementField(
        _('width'),
        measurement=measures.Distance,
        unit_choices=(('centimeter', _('centimeter')),),
    )
    height = MeasurementField(
        _('height'),
        measurement=measures.Distance,
        unit_choices=(('centimeter', _('centimeter')),),
    )
    depth = MeasurementField(
        _('depth'),
        measurement=measures.Distance,
        unit_choices=(('centimeter', _('centimeter')),),
    )

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name


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

    def __unicode__(self):
        return self.measurement
