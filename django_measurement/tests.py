from django.db import models
from django.test import TestCase
from measurement.measures import Distance
from django.forms import Form

from django_measurement.fields import MeasurementField
from django_measurement.forms import MeasurementFormField
from django_measurement import measure, utils


class MeasurementTestModel(models.Model):
    measurement = MeasurementField()

    def __unicode__(self):
        return unicode(self.pk)


class MeasurementTestForm(Form):
    measurement = MeasurementFormField(measurement=Distance, max_value=3.0, min_value=1.0)


class MeasurementFieldTest(TestCase):
    def test_storage_of_standard_measurement(self):
        measurement = measure.Weight(g=20)

        instance = MeasurementTestModel()
        instance.measurement = measurement
        instance.save()

        retrieved = MeasurementTestModel.objects.get(pk=instance.pk)

        self.assertEquals(
            retrieved.measurement,
            measurement
        )

    def test_storage_of_bidimensional_measurement(self):
        measurement = measure.Speed(mph=20)

        instance = MeasurementTestModel()
        instance.measurement = measurement
        instance.save()

        retrieved = MeasurementTestModel.objects.get(pk=instance.pk)

        self.assertEquals(
            retrieved.measurement,
            measurement
        )

    def test_storage_and_retrieval_of_bidimensional_measurement(self):
        arbitrary_default_unit='mi__hr'
        arbitrary_value=65
        arbitrary_measure=measure.Speed
        arbitrary_measurement=utils.get_measurement(
            arbitrary_measure,
            arbitrary_value,
            arbitrary_default_unit,
        )

        instance = MeasurementTestModel.objects.create(
            measurement=arbitrary_measurement
        )
        instance.save()

        retrieved = MeasurementTestModel.objects.all()[0]

        self.assertEqual(
            retrieved.measurement.unit,
            arbitrary_default_unit,
        )
        self.assertEqual(
            retrieved.measurement.__class__,
            arbitrary_measure,
        )
        self.assertAlmostEqual(
            retrieved.measurement.mi__hr,
            arbitrary_value,
        )

    def test_storage_and_retrieval_of_measurement(self):
        arbitrary_default_unit='lb'
        arbitrary_value=124
        arbitrary_measure=measure.Weight
        arbitrary_measurement=utils.get_measurement(
            arbitrary_measure,
            arbitrary_value,
            arbitrary_default_unit,
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

    def test_retrieval_of_mismatched_measure(self):
        arbitrary_default_unit='g'
        arbitrary_measure_name='Weight(a)'
        arbitrary_value=2324

        instance = MeasurementTestModel()
        instance.measurement_value=arbitrary_value
        instance.measurement_measure=arbitrary_measure_name
        instance.measurement_unit=arbitrary_default_unit
        instance.save()

        measurement = MeasurementTestModel.objects.all()[0]

        with self.assertRaises(ValueError):
            measurement.measurement

    def test_retrieval_of_unit_unspecified_measure(self):
        arbitrary_default_unit='g'
        arbitrary_measure_name='Weight'
        arbitrary_value=2324

        instance = MeasurementTestModel()
        instance.measurement_value=arbitrary_value
        instance.measurement_measure=arbitrary_measure_name
        instance.measurement_unit=arbitrary_default_unit
        instance.save()

        retrieved = MeasurementTestModel.objects.all()[0]

        weight = measure.Weight(
            g=arbitrary_value
        )

        self.assertEqual(
            weight,
            retrieved.measurement
        )

    def test_retrieval_of_unknown_measure_returns_unknown_measure(self):
        arbitrary_default_unit='versta'
        arbitrary_measure_name='ImperialRussian(versta)'
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
        arbitrary_measure_name='ImperialRussian(versta)'
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

    def test_max_value(self):
        valid_form = MeasurementTestForm({'measurement_0': 2.0, 'measurement_1': 'mi'})
        invalid_form = MeasurementTestForm({'measurement_0': 4.0, 'measurement_1': 'mi'})
        self.assertTrue(valid_form.is_valid())
        self.assertFalse(invalid_form.is_valid())




class MeasurementUtilsTest(TestCase):
    def test_guess_measurement_weight(self):
        expected_measurement = measure.Weight(mcg=101)
        actual_measurement = utils.guess_measurement(
            101,
            'mcg',
        )

        self.assertEqual(
            expected_measurement,
            actual_measurement,
        )

    def test_guess_measurement_distance(self):
        expected_measurement = measure.Distance(mi=2144)
        actual_measurement = utils.guess_measurement(
            2144,
            'mi',
        )

        self.assertEqual(
            expected_measurement,
            actual_measurement,
        )

    def test_get_measurement(self):
        expected_measurement = measure.Volume(us_qt=34)
        actual_measurement = utils.get_measurement(
            measure.Volume,
            34,
            'us_qt',
        )

        self.assertEqual(
            expected_measurement,
            actual_measurement,
        )

