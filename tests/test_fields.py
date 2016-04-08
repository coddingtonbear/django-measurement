# -*- coding: utf-8 -*-

import pytest
from django.core.exceptions import ValidationError
from django.utils import module_loading
from django.utils.encoding import force_bytes, force_text
from measurement import measures
from measurement.measures import Distance

from django_measurement.forms import MeasurementField
from tests.forms import (
    BiDimensionalLabelTestForm, LabelTestForm, MeasurementTestForm, SITestForm
)
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


@pytest.mark.parametrize('fieldname, measure_cls', [
    ('measurement_weight', measures.Weight),
    ('measurement_distance', measures.Distance),
    ('measurement_distance_km', measures.Distance),
    ('measurement_speed', measures.Speed),
    ('measurement_temperature', measures.Temperature),
    ('measurement_speed_mph', measures.Speed),
])
class TestDeconstruct(object):
    def test_deconstruct(self, fieldname, measure_cls):
        field = MeasurementTestModel._meta.get_field(fieldname)

        name, path, args, kwargs = field.deconstruct()

        assert name == fieldname
        assert path == 'django_measurement.models.MeasurementField'
        assert args == []
        assert kwargs['blank'] == field.blank
        assert kwargs['null'] == field.null
        assert kwargs['measurement_class'] == measure_cls.__name__
        assert kwargs['measurement_class'] == field.measurement_class

        new_cls = module_loading.import_string(path)
        new_field = new_cls(name=name, *args, **kwargs)

        assert type(field) == type(new_field)
        assert field.deconstruct() == (
            name, path, args, kwargs
        )

    def test_deconstruct_old_migrations(self, fieldname, measure_cls):
        field = MeasurementTestModel._meta.get_field(fieldname)

        name, path, args, kwargs = field.deconstruct()

        # replace str class with binary
        kwargs['measurement_class'] = force_bytes(kwargs['measurement_class'])

        new_cls = module_loading.import_string(path)
        new_field = new_cls(name=name, *args, **kwargs)

        assert type(field) == type(new_field)

        _, _, _, kwargs_new = field.deconstruct()

        # kwargs get corrected, cls is a str again
        assert (
            kwargs_new['measurement_class'] ==
            force_text(kwargs['measurement_class'])
        )


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

        field = MeasurementField(measures.Distance, max_value=measures.Distance(mi=1))
        field.clean([0.5, 'mi'])
        with pytest.raises(ValidationError) as e:
            field.clean([2.0, 'mi'])
            assert 'Ensure this value is less than or equal to 1.0 mi.' in force_text(e)

        with pytest.raises(ValueError) as e:
            MeasurementField(measures.Distance, max_value=1.0)
            assert force_text(e) == '"max_value" must be a measure, got float'

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

    def test_min_value(self):
        field = MeasurementField(measures.Distance, min_value=measures.Distance(mi=1.0))
        field.clean([2.0, 'mi'])
        with pytest.raises(ValidationError) as e:
            field.clean([0.5, 'mi'])
            assert 'Ensure this value is greater than or equal to 1.0 mi.' in force_text(e)

        with pytest.raises(ValueError) as e:
            MeasurementField(measures.Distance, min_value=1.0)
            assert force_text(e) == '"min_value" must be a measure, got float'

    def test_float_casting(self, capturelog):
        m = MeasurementTestModel(
            measurement_distance=float(2000),
            measurement_distance_km=2,
        )
        m.full_clean()

        assert m.measurement_distance.value == 2000
        assert m.measurement_distance.unit == Distance.STANDARD_UNIT

        assert m.measurement_distance_km.value == 2
        assert m.measurement_distance_km.unit == 'km'
        assert m.measurement_distance_km == Distance(km=2)

        m.measurement_distance_km = Distance(km=1)
        m.full_clean()
        assert m.measurement_distance_km.value == 1
        assert m.measurement_distance_km.unit == 'km'
        assert m.measurement_distance_km == Distance(km=1)

        record = capturelog.records()[0]

        assert record.levelname == 'WARNING'
        assert record.message == ('You assigned a float instead of Distance to'
                                  ' tests.models.MeasurementTestModel.measurement_distance,'
                                  ' unit was guessed to be "m".')

    def test_unicode_labels(self):
        form = LabelTestForm()
        assert ('c', u'°C') in form.fields['simple'].fields[1].choices
        assert ('f', u'°F') in form.fields['simple'].fields[1].choices
        assert ('k', u'°K') in form.fields['simple'].fields[1].choices

        si_form = SITestForm()
        assert ('ms', 'ms') in si_form.fields['simple'].fields[1].choices
        assert ('Ps', 'Ps') in si_form.fields['simple'].fields[1].choices

        bi_dim_form = BiDimensionalLabelTestForm()
        assert ('c__ms', u'°C__ms') in bi_dim_form.fields['simple'].fields[1].choices
        assert ('c__Ps', u'°C__Ps') in bi_dim_form.fields['simple'].fields[1].choices
