from django.core.validators import DecimalValidator


class MeasurementValidator(DecimalValidator):
    def __call__(self, value):
        super().__call__(value.si_value)
