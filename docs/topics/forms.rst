
Using Measurement Objects in Forms
==================================

Measurement objects need some help in forms because they break Django's normal assumption of a direct relationship between database field and form field (since measurement objects have 3 database columns each).

This is accomplished with the MeasurementFormMixin::

    from django_measurement.forms import MeasurementFormField, MeasurementFormMixin 

    class BeerForm(MeasurementFormMixin, ModelForm):

        volume = MeasurementFormField(measurement=Volume)  

        def __init__(self,*args,**kwargs):
            super (BeerForm, self).__init__(*args,**kwargs)
            self.fields['volume'].label="Volume"


You can limit the units in the select field by using the 'choices' keyword::

    class BeerForm(MeasurementFormMixin, ModelForm):

        volume = MeasurementFormField( measurement=Volume, choices=(("l","l"), ("oz","oz")))
 


