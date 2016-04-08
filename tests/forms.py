from django import forms
from tests.models import MeasurementTestModel
from django_measurement.forms import MeasurementField
from .custom_measure_base import Temperature, Time, DegreePerTime


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
