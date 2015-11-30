from django import forms
from tests.models import MeasurementTestModel


class MeasurementTestForm(forms.ModelForm):
    class Meta:
        model = MeasurementTestModel
        exclude = []
