# -*- coding:utf-8 -*-
from __future__ import (absolute_import, unicode_literals)

from django import forms
from warnings import warn
from measurement.base import MeasureBase
from django.contrib import gis
from . import utils


class MeasurementWidget(forms.MultiWidget):
    def __init__(self, attrs=None, float_widget=None,
                 choices_widget=None, choices=None, *args, **kwargs):
        if not float_widget:
            float_widget = forms.TextInput(attrs=attrs)
        if not choices_widget:
            choices_widget = forms.Select(attrs=attrs, choices=choices)
        widgets = (float_widget, choices_widget)
        super(MeasurementWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            magnitude = getattr(value, value._default_unit)
            # TODO: this should be the unit that was entered by the user
            unit = value._default_unit
            return [magnitude, unit]
        return [None, None]


class MeasurementFormField(forms.MultiValueField):
    def __init__(self, measurement, max_value=None, min_value=None, choices=None,
                 *args, **kwargs):
        if not issubclass(measurement, MeasureBase):
            raise ValueError("%s must be a subclass ov MeasureBase" % measurement)
        self.measurement_class = measurement
        if not choices:
            choices = tuple(((u, u) for u in measurement.UNITS))

        float_field = forms.FloatField(max_value, min_value, *args, **kwargs)
        choice_field = forms.ChoiceField(choices=choices)
        defaults = {
            'widget': MeasurementWidget(float_widget=float_field.widget,
                                        choices_widget=choice_field.widget,
                                        choices=choices),
        }
        defaults.update(kwargs)
        fields = (float_field, choice_field)
        super(MeasurementFormField, self).__init__(fields, *args, **defaults)

    def compress(self, data_list):
        """
        Return a single value for the given list of values.
        The values can be assumed to be valid.
        """
        v = data_list[0]
        if v in self.empty_values:
            return None
        rv = utils.get_measurement(self.measurement_class, data_list[0], data_list[1])
        return rv


class MeasurementFormMixin(object):
    """
    This mixin works around django's preference
    for db fields mapping to form fields
    """

    def __init__(self, *args, **kwargs):
        """
        add fields to initial data
        (so the widgets will start with thre current values) if we have an instance.
        model_to_dict skips over the measurement fields
        because they are not editable (and it sees them as each
        of the 3 database fields that make up a measurement,
        instead of the actual measurement itself
        """
        warn(DeprecationWarning, "MeasurementFormMixin is deprecated"
                                 " and will be removed in versin 1.5")
        super(MeasurementFormMixin, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        due to the way construct_instance looks at database
        fields in the object and skips MeasurementFields
        this function must explicitly update the instance
        with cleaned data before calling the normal save
        """
        for (field_name, value) in self.cleaned_data.items():
            if isinstance(value, MeasureBase) or \
                    isinstance(value, gis.measure.MeasureBase):
                setattr(self.instance, field_name, value)
        return super(MeasurementFormMixin, self).save(commit)
