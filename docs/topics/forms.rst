
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
 
If unicode symbols are needed in the labels for a MeasurementField, define a LABELS dictionary for your subclassed MeasureBase object::

    # -*- coding: utf-8 -*-
    from sympy import S, Symbol
    
    class Temperature(MeasureBase):
        SU = Symbol('kelvin')
        STANDARD_UNIT = 'k'
        UNITS = {
            'c': SU - S(273.15),
            'f': (SU - S(273.15)) * S('9/5') + 32,
            'k': 1.0
        }
        LABELS = {
            'c':u'°C',
            'f':u'°F',
            'k':u'°K',
        }
        
For a `MeasurementField` that represents a `BidimensionalMeasure`, you can set the separator either in settings.py (`BIDIMENSIONAL_SEPARATOR is '/'` by default, add setting to override for all BiDimensionalMeasure subclasses) or override for an individual field with the kwarg bidimensional_separator::

        speed = MeasurementField(
            measurement=Speed,
            bidimensional_separator=' per '
        )
        
        # Rendered option labels will now be in the format "ft per s", "m per hr", etc
