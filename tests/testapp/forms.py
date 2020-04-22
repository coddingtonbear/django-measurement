from django import forms

from django_measurement.forms import MeasurementField
from tests.testapp.models import MeasurementTestModel

from measurement import measures


class MeasurementTestForm(forms.ModelForm):
    class Meta:
        model = MeasurementTestModel
        exclude = []


class LabelTestForm(forms.Form):
    simple = MeasurementField(measures.Temperature)


class SITestForm(forms.Form):
    simple = MeasurementField(measures.Time)


class BiDimensionalLabelTestForm(forms.Form):
    simple = MeasurementField(measures.Volume)
