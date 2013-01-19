from django.db import models
from django.test import TestCase

from fields import MeasurementField
import measure

class MeasurementTestModel(models.Model):
    measurement = MeasurementField()

    def __unicode__(self):
        return unicode(self.pk)

class MeasurementFieldTest(TestCase):
    def test_storage_and_retrieval_of_measurement(self):
        arbitrary_default_unit='lb'
        arbitrary_value=124
        arbitrary_measure=measure.Weight
        arbitrary_measurement=arbitrary_measure(
            **{arbitrary_default_unit: arbitrary_value}
        )

        instance = MeasurementTestModel.objects.create(
            measurement=arbitrary_measurement
        )
        instance.save()

        retrieved = MeasurementTestModel.objects.all()[0]

        self.assertEqual(
            retrieved.measurement._default_unit,
            arbitrary_default_unit,
        )
        self.assertEqual(
            retrieved.measurement.__class__,
            arbitrary_measure,
        )
        self.assertAlmostEqual(
            retrieved.measurement.lb,
            arbitrary_value,
        )

    def test_retrieval_of_unknown_measure_returns_unknown_measure(self):
        arbitrary_default_unit='versta'
        arbitrary_measure_name='ImperialRussian'
        arbitrary_value=3731.5

        instance = MeasurementTestModel()
        instance.measurement_value=arbitrary_value
        instance.measurement_measure=arbitrary_measure_name
        instance.measurement_unit=arbitrary_default_unit
        instance.save()

        retrieved = MeasurementTestModel.objects.all()[0]

        self.assertIsInstance(
            retrieved.measurement,
            measure.UnknownMeasure
        )

    def test_storage_of_unknown_measure_stores_same_measure(self):
        arbitrary_default_unit='versta'
        arbitrary_measure_name='ImperialRussian'
        arbitrary_value=3731.5

        instance = MeasurementTestModel()
        instance.measurement_value=arbitrary_value
        instance.measurement_measure=arbitrary_measure_name
        instance.measurement_unit=arbitrary_default_unit
        instance.save()

        retrieved = MeasurementTestModel.objects.all()[0]

        new = MeasurementTestModel.objects.create(
            measurement=retrieved.measurement
        )

        first = MeasurementTestModel.objects.all()[0]
        second = MeasurementTestModel.objects.all()[1]

        self.assertEqual(
            first.measurement,
            second.measurement,
        )
