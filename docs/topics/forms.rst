
Using Measurement Objects in Forms
==================================

This is an example for a simple form field usage::

    from django import forms
    from django_measurement.forms import MeasurementField

    class BeerForm(forms.Form):

        volume = MeasurementField(Volume)

You can limit the units in the select field by using the 'unit_choices' keyword argument.
To limit the value choices of the MeasurementField uses the regular 'choices' keyword argument::

    class BeerForm(forms.Form):

        volume = MeasurementField(
            measurement=Volume,
            unit_choices=(("l","l"), ("oz","oz")),
            choices=((1.0, 'one'), (2.0, 'two'))
        )
 
