.. image:: https://travis-ci.org/latestrevision/django-measurement.png?branch=master

A simple Django app providing for
a simple way of using and storing weights and measures.

Installation
============

You can either install from pip::

    pip install django-measurement

*or* checkout and install the source from the `bitbucket repository <https://bitbucket.org/latestrevision/django-measurement/>`_::

    hg clone https://bitbucket.org/latestrevision/django-measurement
    cd django-measurement
    python setup.py install

*or* checkout and install the source from the `github repository <https://github.com/latestrevision/django-measurement/>`_::

    git clone https://github.com/latestrevision/django-measurement.git
    cd django-measurement
    python setup.py install


Measures
========

This application provides the following measures:

+-------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+------------------------------------------+
| Measurement | Units Accepted                                                                                                                                                                                                                                                                                                                                                                                               | Standard Unit | Notes                                    |
+=============+==============================================================================================================================================================================================================================================================================================================================================================================================================+===============+==========================================+
| Distance    | chain, chain_benoit, chain_sears, british_chain_benoit, british_chain_sears, british_chain_sears_truncated, cm, british_ft, british_yd, clarke_ft, clarke_link, fathom, ft, german_m, gold_coast_ft, indian_yd, inch, km, link, link_benoit, link_sears, m, mi, mm, nm, nm_uk, rod, sears_yd, survey_ft, um, yd                                                                                              | m             | Provided by `django.contrib.gis.measure` |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+------------------------------------------+
| Area        | sq_chain, sq_chain_benoit, sq_chain_sears, sq_british_chain_benoit, sq_british_chain_sears, sq_british_chain_sears_truncated, sq_cm, sq_british_ft, sq_british_yd, sq_clarke_ft, sq_clarke_link, sq_fathom, sq_ft, sq_german_m, sq_gold_coast_ft, sq_indian_yd, sq_inch, sq_km, sq_link, sq_link_benoit, sq_link_sears, sq_m, sq_mi, sq_mm, sq_nm, sq_nm_uk, sq_rod, sq_sears_yd, sq_survey_ft, sq_um, sq_yd | sq_m          | Provided by `django.contrib.gis.measure` |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+------------------------------------------+
| Weight      | mcg, mg, g, kg, tonne, oz, lb, stone, short_ton, long_ton                                                                                                                                                                                                                                                                                                                                                    | g             |                                          |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+------------------------------------------+
| Volume      | us_g, us_qt, us_pint, us_cup, us_oz, us_tbsp, us_tsp, cubic_centimeter, cubic_meter, l, ml, cubic_foot, cubic_inch, imperial_g, imperial_qt, imperial_pint, imperial_oz, imperial_tbsp, imperial_tsp                                                                                                                                                                                                         | cubic_meter   |                                          |
+-------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+------------------------------------------+


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


Storing Measurement Objects
===========================

Suppose you were trying to cut back on drinking,
and needed to store a log of how much beer you drink day-to-day;
you might (naively) create a model like such::

    from django_measurement.fields import MeasurementField
    from django.db.models import Model

    class BeerConsumptionLogEntry(Model):
        name = models.CharField(max_length=255)
        volume = models.MeasurementField()

        def __str__(self):
            return '%s of %s' % (self.name, self.volume, )

and assume you had a pint of 
`Ninkasi's Total Domination <http://www.ninkasibrewing.com/beers/total_domination>`_;
you'd add it to your log like so::

    from django_measurement.measure import Volume

    beer = BeerConsumptionLogEntry()
    beer.name = 'Total Domination'
    beer.volume = Volume(us_pint=1)
    beer.save()

    print beer # '1 us_pint of Total Domination'

Perhaps you next recklessly dove into your stash of terrible,
but nostalgia-inducing Russian beer and had a half-liter of
`Baltika's #9 <http://beeradvocate.com/beer/profile/401/1967>`_;
you'd add it to your log like so::

    another_beer = BeerConsumptionLogEntry()
    another_beer.name = '#9'
    another_beer.volume = Volume(l=0.5)
    another_beer.save()

    print beer # '0.5 l of #9'

Note that although the original unit specified is stored for display,
that the unit is abstracted to the measure's standard unit for storage and comparison::

    print beer.volume                       # '1 us_pint'
    print another_beer.volume               # '0.5 l'
    print beer.volume > another_beer.volume # False


How is this data stored?
========================

In the above example, we created a model field named ``volume``, 
this would be realized in three columns:

- ``volume_unit``: Stores the originally-specified unit.
- ``volume_measure``: Stores the measurement's measure ('Weight', 'Volume', 'Distance', etc.).
- ``volume_value``: Stores the float value of the measurement in the measure's standard unit.

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
Be sure to look at ``django-measurement/measure.py`` for examples of what
makes a measurement class.

