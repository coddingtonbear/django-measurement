from typing import Type

from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter
from django.db.models import DecimalField
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from . import forms, utils, validators

from measurement.base import AbstractMeasure


class MeasureSerializer(BaseSerializer):
    def serialize(self):
        return (
            repr(self.value),
            {f"from measurement.measures import {type(self.value).__qualname__}"},
        )


MigrationWriter.register_serializer(AbstractMeasure, MeasureSerializer)


class MeasurementField(DecimalField):
    description = "Easily store, retrieve, and convert python measures."
    empty_strings_allowed = False
    default_error_messages = {
        "invalid_type": _(
            "'%(value)s' (%(type_given)s) value" " must be of type %(type_wanted)s."
        ),
    }

    def __init__(self, *args, measure: Type[AbstractMeasure] = None, **kwargs):

        self.measure = measure
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(MeasurementField, self).deconstruct()
        kwargs["measure"] = self.measure
        return name, path, args, kwargs

    def get_prep_value(self, value):
        if value is not None:
            return value.si_value

    def get_default_unit(self):
        return next(iter(self.measure._units.keys()))

    def from_db_value(self, value, *args, **kwargs):
        if value is not None:
            return utils.get_measurement(measure=self.measure, value=value,)

    def value_to_string(self, obj):
        return str(self.value_from_object(obj))

    def get_db_prep_save(self, value, connection):
        value = self.to_python(value)
        if isinstance(value, AbstractMeasure):
            value = value.si_value
        return connection.ops.adapt_decimalfield_value(
            value, self.max_digits, self.decimal_places
        )

    def to_python(self, value):
        return value

    def deserialize_value_from_string(self, s: str):
        return self.measure(s)

    def formfield(self, **kwargs):
        return super().formfield(
            **{"form_class": forms.MeasurementField, "measure": self.measure, **kwargs,}
        )

    @cached_property
    def validators(self):
        return [
            *self.default_validators,
            *self._validators,
            validators.MeasurementValidator(self.max_digits, self.decimal_places),
        ]
