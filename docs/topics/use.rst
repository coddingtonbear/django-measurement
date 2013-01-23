
Using Measurement Objects
=========================

You can import any of the above measures from `django_measurement.measure` 
and use it for easily handling measurements like so::

    from django_measurement.measure import Weight

    w = Weight(lb=135) # Represents 135lbs
    print w            # '135.0 lb'
    print w.kg         # '61.234919999999995'

See `Django's documentation on Measurement Objects <https://docs.djangoproject.com/en/dev/ref/contrib/gis/measure/>`_ 
for more information about interacting with measurements.

