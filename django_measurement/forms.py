from django import forms
import django_measurement.utils
import django_measurement.base
import django.contrib.gis.measure

from django_measurement.fields import MeasurementField

import inspect

class MeasurementWidget(forms.MultiWidget):

    def __init__(self, attrs=None, choices=(), *args, **kwargs):
        widgets = ( forms.TextInput(attrs=attrs), forms.Select(attrs=attrs, choices=choices) )
        super(MeasurementWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            magnitude = getattr( value, value._default_unit)
            unit = value._default_unit # TODO: this should be the unit that was entered by the user
            return [ magnitude, unit ]
        return [None, None]



class MeasurementFormField(forms.MultiValueField):

    def __init__(self, *args, **kwargs):
        self.measurement_class = kwargs.pop("measurement", None)
        if not self.measurement_class:
            raise Exception("MeasurementFormField requires 'measurement'=<measurement class> keyword arguement")
        choices = kwargs.pop("choices", None)
        if not choices:
            choices=tuple( ((u, u) for u in self.measurement_class.UNITS))
        defaults={'widget': MeasurementWidget(choices=choices)}
        defaults.update(kwargs)
        fields = ( forms.FloatField(), forms.ChoiceField(choices=choices) ) # have to pass in the fields or you'l get no data
        super(MeasurementFormField, self).__init__( fields, *args, **defaults)

    def compress(self, data_list):
        """
        Return a single value for the given list of values. The values can be
        assumed to be valid.
        """
        v = data_list[0]
        if v==None or v=="" or (isinstance(v, str) and v.strip()==""):
            return None 
        rv = django_measurement.utils.get_measurement( self.measurement_class, data_list[0], data_list[1] )
        return rv


class MeasurementFormMixin(object):
    "This mixin works around django's preference for db fields mapping to form fields"

    def __init__(self, *args, **kwargs):
        """add fields to initial data (so the widgets will start with thre current values) if we have an instance.
           model_to_dict skips over the measurement fields because they are not editable (and it sees them as each
           of the 3 database fields that make up a measurement, instead of the actual measurement itself"""
        instance = kwargs.get("instance", None)
        if instance:
            # have an instance, must update initial data for measure fields as model_to_dict skips them 
            # otherwise edits won't start with current value
            initial = kwargs.get("initial", {})
            measurements = inspect.getmembers(instance, lambda x: isinstance(x, django_measurement.base.MeasureBase) or isinstance(x, django.contrib.gis.measure.MeasureBase) or isinstance(x, MeasurementField))
            for (name, value) in measurements:
                initial[name] = value
            kwargs["initial"]=initial
        super(MeasurementFormMixin, self).__init__(*args, **kwargs)


    def save(self, commit=True):
        """due to the way construct_instance looks at database fields in the object and skips MeasurementFields
           this function must explicitly update the instance with cleaned data before calling the normal save"""
        for (field_name, value) in self.cleaned_data.items():
            if isinstance( value, django_measurement.base.MeasureBase) or \
               isinstance( value, django.contrib.gis.measure.MeasureBase):
                    setattr( self.instance, field_name, value) 
        return super(MeasurementFormMixin, self).save(commit)
