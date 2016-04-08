from django import forms

from django_measurement.forms import MeasurementField
from tests.custom_measure_base import DegreePerTime, Temperature, Time
from tests.models import MeasurementTestModel


class MeasurementTestForm(forms.ModelForm):
    class Meta:
        model = MeasurementTestModel
        exclude = []


class LabelTestForm(forms.Form):
    simple = MeasurementField(Temperature)


class SITestForm(forms.Form):
    simple = MeasurementField(Time)


class BiDimensionalLabelTestForm(forms.Form):
    simple = MeasurementField(DegreePerTime)
