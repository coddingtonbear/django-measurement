from typing import Type

from django import forms
from django.core.exceptions import ValidationError
from django.utils import formats

from django_measurement.validators import MeasurementValidator

from measurement.base import AbstractMeasure


class MeasurementField(forms.DecimalField):
    widget = forms.TextInput

    def __init__(self, measure: Type[AbstractMeasure] = None, **kwargs):
        self.measure: Type[AbstractMeasure] = measure
        super().__init__(**kwargs)
        self.validators = [
            *self.validators[:-1],
            MeasurementValidator(self.max_digits, self.decimal_places),
        ]

    def validate(self, value):
        forms.Field.validate(self, value)
        if value in self.empty_values:
            return
        if not value.si_value.is_finite():
            raise ValidationError(self.error_messages["invalid"], code="invalid")

    def to_python(self, value):
        if value in self.empty_values:
            return None
        if self.localize:
            value = formats.sanitize_separators(value)
        value = str(value).strip()
        try:
            value = self.measure(value)
        except (TypeError, ValueError):
            raise ValidationError(self.error_messages["invalid"], code="invalid")
        return value
