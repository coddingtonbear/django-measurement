import pytest
from measurement import measures
from tests.forms import MeasurementTestForm
from tests.models import MeasurementTestModel

pytestmark = [
    pytest.mark.django_db,
]


class TestMeasurementField(object):
    def test_storage_of_standard_measurement(self):
        measurement = measures.Weight(g=20)

        instance = MeasurementTestModel()
        instance.measurement_weight = measurement
        instance.save()

        retrieved = MeasurementTestModel.objects.get(pk=instance.pk)

        assert retrieved.measurement_weight == measurement

    def test_storage_of_temperature(self):
        measurement = measures.Temperature(c=20)

        instance = MeasurementTestModel()
        instance.measurement_temperature = measurement
        instance.save()

        retrieved = MeasurementTestModel.objects.get(pk=instance.pk)

        assert retrieved.measurement_temperature == measurement

    def test_storage_of_string_value(self):
        instance = MeasurementTestModel()
        instance.measurement_weight = "21.4"
        instance.save()

        retrieved = MeasurementTestModel.objects.get(pk=instance.pk)

        assert retrieved.measurement_weight == measures.Weight(g=21.4)

    def test_storage_of_float_value(self):
        instance = MeasurementTestModel()
        instance.measurement_weight = 21.4
        instance.save()

        retrieved = MeasurementTestModel.objects.get(pk=instance.pk)

        assert retrieved.measurement_weight == measures.Weight(g=21.4)

    def test_storage_of_bidimensional_measurement(self):
        measurement = measures.Speed(mph=20)

        instance = MeasurementTestModel()
        instance.measurement_speed = measurement
        instance.save()

        retrieved = MeasurementTestModel.objects.get(pk=instance.pk)

        assert retrieved.measurement_speed == measurement

    def test_storage_and_retrieval_of_bidimensional_measurement(self):
        original_value = measures.Speed(mph=65)

        MeasurementTestModel.objects.create(
            measurement_speed=original_value,
        )

        retrieved = MeasurementTestModel.objects.get()

        new_value = retrieved.measurement_speed

        assert new_value == original_value
        assert type(new_value) == type(original_value)
        assert new_value.unit == original_value.STANDARD_UNIT

    def test_storage_and_retrieval_of_bidimensional_measurement_choice(self):
        original_value = measures.Speed(mph=65)

        MeasurementTestModel.objects.create(
            measurement_speed_mph=original_value,
        )

        retrieved = MeasurementTestModel.objects.get()

        new_value = retrieved.measurement_speed_mph

        assert new_value == original_value
        assert type(new_value) == type(original_value)
        assert new_value.unit == original_value.unit

    def test_storage_and_retrieval_of_measurement(self):
        original_value = measures.Weight(lb=124)

        MeasurementTestModel.objects.create(
            measurement_weight=original_value,
        )

        retrieved = MeasurementTestModel.objects.get()
        new_value = retrieved.measurement_weight

        assert new_value == original_value
        assert type(new_value) == type(original_value)
        assert new_value.unit == original_value.STANDARD_UNIT

    def test_storage_and_retrieval_of_measurement_choice(self):
        original_value = measures.Distance(km=100)

        MeasurementTestModel.objects.create(
            measurement_distance_km=original_value,
        )

        retrieved = MeasurementTestModel.objects.get()
        new_value = retrieved.measurement_distance_km

        assert new_value == original_value
        assert type(new_value) == type(original_value)
        assert new_value.unit == original_value.unit


class TestMeasurementFormField(object):
    def test_max_value(self):
        valid_form = MeasurementTestForm({
            'measurement_distance_0': 2.0,
            'measurement_distance_1': 'mi',
        })
        invalid_form = MeasurementTestForm({
            'measurement_distance_0': 4.0,
            'measurement_distance_1': 'mi',
        })
        assert valid_form.is_valid()
        assert not invalid_form.is_valid()

    def test_form_storage(self):
        form = MeasurementTestForm({
            'measurement_distance_0': 2.0,
            'measurement_distance_1': 'mi',
        })
        assert form.is_valid()
        obj = form.save()

        assert obj.measurement_distance == measures.Distance(mi=2)

    def test_form_bidir(self):
        form = MeasurementTestForm({
            'measurement_speed_0': 2.0,
            'measurement_speed_1': 'mi__hr',
        })
        assert form.is_valid()
        obj = form.save()

        assert obj.measurement_speed == measures.Speed(mi__hr=2)
