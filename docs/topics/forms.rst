
Using Measurement Objects in Forms
==================================

This is an example for a simple form field usage::

    from django import forms
    from django_measurement.forms import MeasurementField

    class BeerForm(forms.Form):

        volume = MeasurementField(Volume)
