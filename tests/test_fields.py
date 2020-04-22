import pytest
from django.core import serializers
from django.core.exceptions import ValidationError
from django.utils import module_loading

from django_measurement.forms import MeasurementField
from tests.testapp.forms import MeasurementTestForm
from tests.testapp.models import MeasurementTestModel

from measurement import measures

pytestmark = [
    pytest.mark.django_db,
]


class TestMeasurementField:
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

        MeasurementTestModel.objects.create(measurement_speed=original_value,)

        retrieved = MeasurementTestModel.objects.get()

        new_value = retrieved.measurement_speed

        assert new_value == original_value
        assert type(new_value) == type(original_value)
        assert new_value.unit == original_value.STANDARD_UNIT

    def test_storage_and_retrieval_of_bidimensional_measurement_choice(self):
        original_value = measures.Speed(mph=65)

        MeasurementTestModel.objects.create(measurement_speed_mph=original_value,)

        retrieved = MeasurementTestModel.objects.get()

        new_value = retrieved.measurement_speed_mph

        assert new_value == original_value
        assert type(new_value) == type(original_value)
        assert new_value.unit == original_value.unit

    def test_storage_and_retrieval_of_measurement(self):
        original_value = measures.Weight(lb=124)

        MeasurementTestModel.objects.create(measurement_weight=original_value,)

        retrieved = MeasurementTestModel.objects.get()
        new_value = retrieved.measurement_weight

        assert new_value == original_value
        assert type(new_value) == type(original_value)
        assert new_value.unit == original_value.STANDARD_UNIT

    def test_storage_and_retrieval_of_measurement_choice(self):
        original_value = measures.Distance(km=100)

        MeasurementTestModel.objects.create(measurement_distance_km=original_value,)

        retrieved = MeasurementTestModel.objects.get()
        new_value = retrieved.measurement_distance_km

        assert new_value == original_value
        assert type(new_value) == type(original_value)
        assert new_value.unit == original_value.unit


@pytest.mark.parametrize(
    "fieldname, measure_cls",
    [
        ("measurement_mass", measures.Mass),
        ("measurement_distance", measures.Distance),
        ("measurement_distance_km", measures.Distance),
        ("measurement_speed", measures.Speed),
        ("measurement_temperature", measures.Temperature),
        ("measurement_speed_mph", measures.Speed),
        ("measurement_custom_degree_per_time", measures.VolumetricFlowRate),
        ("measurement_custom_temperature", measures.Temperature),
        ("measurement_custom_time", measures.Time),
    ],
)
class TestDeconstruct:
    def test_deconstruct(self, fieldname, measure_cls):
        field = MeasurementTestModel._meta.get_field(fieldname)

        name, path, args, kwargs = field.deconstruct()

        assert name == fieldname
        assert path == "django_measurement.models.MeasurementField"
        assert args == []
        assert kwargs["blank"] == field.blank
        assert kwargs["null"] == field.null
        assert kwargs["measure"] == field.measure

        new_cls = module_loading.import_string(path)
        new_field = new_cls(name=name, *args, **kwargs)

        assert type(field) == type(new_field)
        assert field.deconstruct() == (name, path, args, kwargs)


@pytest.mark.parametrize(
    "fieldname, measure, expected_serialized_value",
    [
        ("measurement_mass", measures.Mass(kg=4.0), "4.0:kg"),
        ("measurement_speed", measures.Speed(mi__hr=2.0), "2.0:mi__hr"),
    ],
)
class TestSerialization:
    def test_deconstruct(self, fieldname, measure, expected_serialized_value):
        instance = MeasurementTestModel(pk=0)
        setattr(instance, fieldname, measure)
        serialized_object = serializers.serialize("python", [instance])[0]
        serialized_value = serialized_object["fields"][fieldname]

        assert isinstance(serialized_value, str)
        assert serialized_value == expected_serialized_value

        deserialized_obj = next(serializers.deserialize("python", [serialized_object]))
        deserialized_value = getattr(deserialized_obj.object, fieldname)

        assert deserialized_value == measure


class TestMeasurementFormField:
    def test_max_value(self):
        valid_form = MeasurementTestForm(
            {"measurement_distance_0": 2.0, "measurement_distance_1": "mi"}
        )
        invalid_form = MeasurementTestForm(
            {"measurement_distance_0": 4.0, "measurement_distance_1": "mi"}
        )
        assert valid_form.is_valid()
        assert not invalid_form.is_valid()

        field = MeasurementField(measures.Distance, max_value=measures.Distance(mi=1))
        field.clean([0.5, "mi"])
        with pytest.raises(ValidationError) as e:
            field.clean([2.0, "mi"])
            assert "Ensure this value is less than or equal to 1.0 mi." in str(e)

        with pytest.raises(ValueError) as e:
            MeasurementField(measures.Distance, max_value=1.0)
            assert bytes(e) == '"max_value" must be a measure, got float'

    def test_form_storage(self):
        form = MeasurementTestForm(
            {"measurement_distance_0": 2, "measurement_distance_1": "mi"}
        )
        assert form.is_valid()
        obj = form.save()

        assert obj.measurement_distance == measures.Distance(mi=2)

    def test_form_bidir(self):
        form = MeasurementTestForm(
            {"measurement_speed_0": 2.0, "measurement_speed_1": "mi__hr"}
        )
        assert form.is_valid()
        obj = form.save()

        assert obj.measurement_speed == measures.Speed(mi__hr=2)

    def test_min_value(self):
        field = MeasurementField(measures.Distance, min_value=measures.Distance(mi=1))
        field.clean(["2 mi"])
        with pytest.raises(ValidationError) as e:
            field.clean(["0.5 mi"])
        assert "Ensure this value is greater than or equal to 1.0 mi." in str(e.value)

        with pytest.raises(ValueError) as e:
            MeasurementField(measures.Distance, min_value=1)
        assert str(e.value) == '"min_value" must be a measure, got float'
