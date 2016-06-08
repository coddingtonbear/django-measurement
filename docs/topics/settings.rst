
Settings
========


``MEASURE_OVERRIDES``
---------------------

If you have your own measures to add, 
you can specify a name for your measure and a string class path to allow
for your custom measure to be properly stored and resurrected.::

    MEASURE_OVERRIDES = {
        'IU': 'path.to.my.class.IUMeasure'
    }

You can also override existing measure classes this way.


``BIDIMENSIONAL_SEPARATOR``
---------------------
For any BidimensionalMeasure, what is placed between the primary and reference dimensions on rendered label

    BIDIMENSIONAL_SEPARATOR = " per "

Defaults to "/". Can be overriden as kwarg `bidimensional_separator` for a given MeasurementField.
