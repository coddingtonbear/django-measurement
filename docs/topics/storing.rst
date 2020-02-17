
Storing Measurement Objects
===========================

Suppose you were trying to cut back on drinking,
and needed to store a log of how much beer you drink day-to-day;
you might (naively) create a model like such::

    from django_measurement.models import MeasurementField
    from measurement.measures import Volume
    from django.db import models

    class BeerConsumptionLogEntry(models.Model):
        name = models.CharField(max_length=255)
        volume = MeasurementField(measurement=Volume)

        def __str__(self):
            return '%s of %s' % (self.name, self.volume)

and assume you had a pint of 
`Ninkasi's Total Domination <http://www.ninkasibrewing.com/beers/total_domination>`_;
you'd add it to your log like so::

    from measurement.measures import Volume

    beer = BeerConsumptionLogEntry()
    beer.name = 'Total Domination'
    beer.volume = Volume(us_pint=1)
    beer.save()

    print(beer)           # '1.0 us_pint of Total Domination'
    print(beer.volume)    # '1.0 us_pint of Total Domination'
    print(beer.volume.l)

Perhaps you next recklessly dove into your stash of terrible,
but nostalgia-inducing Russian beer and had a half-liter of
`Baltika's #9 <http://beeradvocate.com/beer/profile/401/1967>`_;
you'd add it to your log like so::

    another_beer = BeerConsumptionLogEntry()
    another_beer.name = '#9'
    another_beer.volume = Volume(l=0.5)
    another_beer.save()

    print(another_beer) # '0.5 l of #9'

Note that although the original unit specified is stored for display,
that the unit is abstracted to the measure's standard unit for storage and comparison::

    print(beer.volume)                       # '1 us_pint'
    print(beer.volume.l)                     # '0.473176'
    print(another_beer.volume.us_tsp)        # '101.44251252815029'
    print(beer.volume > another_beer.volume) # False


Optional Decimal use
--------------------

By default, django-measurement and python-measurement use float values for storing and 
displaying measures. If you prefer deimals you can add the 'decimal', 'max_digits', and
'decimal_places' arguments to the MeasurementField. The example above becomes::

    from django_measurement.models import MeasurementField
    from measurement.measures import Volume
    from django.db import models

    class BeerConsumptionLogEntry(models.Model):
        name = models.CharField(max_length=255)
        volume = MeasurementField(measurement=Volume, decimal=True, max_digits=12, decimal_places=20)

        def __str__(self):
            return '%s of %s' % (self.name, self.volume)

    beer = BeerConsumptionLogEntry()
    beer.name = 'Total Domination'
    beer.volume = Volume(us_pint=1)
    beer.save()

    another_beer = BeerConsumptionLogEntry()
    another_beer.name = '#9'
    another_beer.volume = Volume(l=0.5)
    another_beer.save()

    print(beer.volume.value)                 # "Decimal('0.00047317600000000')""
    print(another_beer.volume.value)         # "Decimal('0.00050000000000000')"
    print(beer.volume > another_beer.volume) # False


How is this data stored?
------------------------

Since django-measurement v2.1 the value will be stored in a single float field or in a single decimal field if the optional decimal argument is utilized.
