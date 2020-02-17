import decimal as decimal_class
import logging
import warnings

from django.core import checks
from django.db.models import Field, FloatField
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from measurement import measures
from measurement.base import BidimensionalMeasure, MeasureBase

from django_measurement import forms
from django_measurement.utils import get_measurement

logger = logging.getLogger('django_measurement')


class MeasurementField(Field):
    description = "Easily store, retrieve, and convert python measures."
    empty_strings_allowed = False
    MEASURE_BASES = (
        BidimensionalMeasure,
        MeasureBase,
    )
    default_error_messages = {
        'invalid_type': _(
            "'%(value)s' (%(type_given)s) value"
            " must be of type %(type_wanted)s."
        ),
    }

    def __init__(self, verbose_name=None, name=None, measurement=None,
                 max_digits=None, decimal_places=None,
                 measurement_class=None, unit_choices=None, *args, **kwargs):

        if not measurement and measurement_class is not None:
            warnings.warn(
                "\"measurement_class\" will be removed in version 4.0",
                DeprecationWarning
            )
            measurement = getattr(measures, measurement_class)

        if not measurement:
            raise TypeError('MeasurementField() takes a measurement'
                            ' keyword argument. None given.')

        if not issubclass(measurement, self.MEASURE_BASES):
            raise TypeError(
                'MeasurementField() takes a measurement keyword argument.'
                ' It has to be a valid MeasureBase subclass.'
            )

        self.max_digits, self.decimal_places = max_digits, decimal_places
        measurement.decimal = True
        self.measurement = measurement
        self.widget_args = {
            'measurement': measurement,
            'unit_choices': unit_choices,
            'max_digits': max_digits,
            'decimal_places': decimal_places,
        }

        super().__init__(verbose_name, name, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['decimal'] = True
        if self.measurement is not None:
            kwargs['measurement'] = self.measurement
        if self.max_digits is not None:
            kwargs['max_digits'] = self.max_digits
        if self.decimal_places is not None:
            kwargs['decimal_places'] = self.decimal_places
        return name, path, args, kwargs

    def get_prep_value(self, value):
        if value is None:
            return None

        elif isinstance(value, self.MEASURE_BASES):
            # sometimes we get sympy.core.numbers.Float, which the
            # database does not understand, so explicitely convert

            return decimal_class.Decimal(value.standard)

        else:
            return super().get_prep_value(value)

    def get_default_unit(self):
        unit_choices = self.widget_args['unit_choices']
        if unit_choices:
            return unit_choices[0][0]
        return self.measurement.STANDARD_UNIT

    def from_db_value(self, value, *args, **kwargs):
        if value is None:
            return None

        return get_measurement(
            measure=self.measurement,
            value=value,
            original_unit=self.get_default_unit(),
        )

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        if not isinstance(value, self.MEASURE_BASES):
            return value
        return '%s:%s' % (value.value, value.unit)

    def deserialize_value_from_string(self, s: str):
        parts = s.split(':', 1)
        if len(parts) != 2:
            return None
        value, unit = decimal_class.Decimal(parts[0]), parts[1]
        measure = get_measurement(self.measurement, value=value, unit=unit)
        return measure

    def to_python(self, value):
        if value is None:
            return value
        elif isinstance(value, self.MEASURE_BASES):
            return value
        elif isinstance(value, str):
            parsed = self.deserialize_value_from_string(value)
            if parsed is not None:
                return parsed
        value = super().to_python(value)

        return_unit = self.get_default_unit()

        msg = "You assigned a %s instead of %s to %s.%s.%s, unit was guessed to be \"%s\"." % (
            type(value).__name__,
            str(self.measurement.__name__),
            self.model.__module__,
            self.model.__name__,
            self.name,
            return_unit,
        )
        logger.warning(msg)
        return get_measurement(
            measure=self.measurement,
            value=value,
            unit=return_unit,
        )

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.MeasurementField, 'max_digits': self.max_digits,
                    'decimal_places': self.decimal_places}
        defaults.update(kwargs)
        defaults.update(self.widget_args)
        return super().formfield(**defaults)

    def get_internal_type(self):
        return "DecimalField"

    @cached_property
    def context(self):
        return decimal_class.Context(prec=self.max_digits)

    def check(self, **kwargs):
        errors = super().check(**kwargs)

        digits_errors = [
            *self._check_decimal_places(),
            *self._check_max_digits(),
        ]
        if not digits_errors:
            errors.extend(self._check_decimal_places_and_max_digits(**kwargs))
        else:
            errors.extend(digits_errors)
        return errors

    def _check_decimal_places(self):
        try:
            decimal_places = int(self.decimal_places)
            if decimal_places < 0:
                raise ValueError()
        except TypeError:
            return [
                checks.Error(
                    "DecimalFields must define a 'decimal_places' attribute.",
                    obj=self,
                    id='fields.E130',
                )
            ]
        except ValueError:
            return [
                checks.Error(
                    "'decimal_places' must be a non-negative integer.",
                    obj=self,
                    id='fields.E131',
                )
            ]
        else:
            return []

    def _check_max_digits(self):
        try:
            max_digits = int(self.max_digits)
            if max_digits <= 0:
                raise ValueError()
        except TypeError:
            return [
                checks.Error(
                    "DecimalFields must define a 'max_digits' attribute.",
                    obj=self,
                    id='fields.E132',
                )
            ]
        except ValueError:
            return [
                checks.Error(
                    "'max_digits' must be a positive integer.",
                    obj=self,
                    id='fields.E133',
                )
            ]
        else:
            return []

    def _check_decimal_places_and_max_digits(self, **kwargs):
        if int(self.decimal_places) > int(self.max_digits):
            return [
                checks.Error(
                    "'max_digits' must be greater or equal to 'decimal_places'.",
                    obj=self,
                    id='fields.E134',
                )
            ]
        return []
