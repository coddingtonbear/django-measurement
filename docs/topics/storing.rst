
Storing Measurement Objects
===========================

Suppose you were trying to cut back on drinking,
and needed to store a log of how much beer you drink day-to-day;
you might (naively) create a model like such::

    from django_measurement.fields import MeasurementField
    from django.db.models import Model

    class BeerConsumptionLogEntry(Model):
        name = models.CharField(max_length=255)
        volume = models.MeasurementField(Volume)

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
------------------------

Since django-measurement v2.0 there value will be stored in a single float field.