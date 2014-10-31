from django.db import models
from django_measurement import fields, measure


class MeasurementTestModel(models.Model):
    measurement = fields.MeasurementField(measurement=measure.Distance,
                                          max_value=3.0, min_value=1.0)

    def __unicode__(self):
        return self.measurement
