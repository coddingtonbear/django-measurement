import decimal
from rest_framework import serializers


def is_valid_unit(unit_to_validate, measurement_class):
    return unit_to_validate in measurement_class.get_units()


def is_valid_decimal(value_to_validate):
    return decimal.Decimal(value_to_validate)


class MeasurementSerializerField(serializers.Field):
    '''
    Serializer field to be used with [Django Rest Framework](https://www.django-rest-framework.org/) serializers.
    Could be used with different kind of measures as shown below:

    ## Example of use:
    ```python
        from rest_framework import serializers
        from measurement.measures import Distance, Weight
        from measurement.rest_framework import MeasurementSerializerField
        from .models import ProductDimensions


        class ProductDimensionsSerializer(serializers.ModelSerializer): 
            width = MeasurementSerializerField(measurement_class=Distance, required=False, allow_null=True)
            height = MeasurementSerializerField(measurement_class=Distance, required=False, allow_null=True)
            length = MeasurementSerializerField(measurement_class=Distance, required=False, allow_null=True)
            weight = MeasurementSerializerField(measurement_class=Weight, required=False, allow_null=True)

            class Meta:
                model = ProductVariantPhysicalDimensions
                fields = ["width", "height", "length", "weight"]
    ```
    '''

    def __init__(self, measurement_class, *args, **kwargs):
        super(MeasurementSerializerField, self).__init__(*args, **kwargs)
        self.measurement_class = measurement_class

    def to_representation(self, obj):
        return {
            'unit': obj.unit,
            'value': obj.value
        }

    default_error_messages = {
        'invalid_unit': 'Invalid unit. {invalid_unit} is not a valid {measurement_class.__name__} unit',
        'invalid_value': 'Invalid value. {invalid_value} is not a valid {measurement_class.__name__} value',
    }

    def to_internal_value(self, data):
        if not is_valid_unit(data['unit'], self.measurement_class):
            self.fail(
                'invalid_unit',
                invalid_unit=data['unit'],
                measurement_class=self.measurement_class
            )

        if not is_valid_decimal(data['value']):
            self.fail(
                'invalid_value',
                invalid_value=data['value'],
                measurement_class=self.measurement_class
            )

        return self.measurement_class(**{data['unit']: data['value']})
