.. image:: https://travis-ci.org/latestrevision/django-measurement.png?branch=master
   :target: https://travis-ci.org/latestrevision/django-measurement

Easily use, manipulate, and store unit-aware measurement objects using Python
and Django.

`django.contrib.gis.measure <https://github.com/django/django/blob/master/django/contrib/gis/measure.py>`_
has these wonderful 'Distance' objects that can be used not only for storing a
unit-aware distance measurement, but also for converting between different
units and adding/subtracting these objects from one another.

This module provides for a django model field and admin interface for storing
any measurements provided by `python-measurement <https://github.com/latestrevision/python-measurement>`_.

Example use with a model:

.. code-block:: python

   from django_measurement.fields import MeasurementField
   from measurement.measures import Volume
   from django.db.models import Model
   
   class BeerConsumptionLogEntry(Model):
       name = models.CharField(max_length=255)
       volume = models.MeasurementField()
   
       def __str__(self):
           return '%s of %s' % (self.name, self.volume, )

   entry = BeerConsumptionLogEntry()
   entry.name = 'Bear Republic Racer 5'
   entry.volume = Volume(us_pint=1)
   entry.save()

These stored measurement objects can be used in all of the usual ways supported
by `python-measurement <https://github.com/latestrevision/python-measurement>`_
too:

.. code-block:: python

   >>> from measurement.measures import Weight
   >>> weight_1 = Weight(lb=125)
   >>> weight_2 = Weight(kg=40)
   >>> added_together = weight_1 + weight_2
   >>> added_together
   Weight(lb=213.184976807)
   >>> added_together.kg  # Maybe I actually need this value in kg?
   96.699

- Documentation for django-measurement is available an
  `ReadTheDocs <http://django-measurement.readthedocs.org/>`_.
- Please post issues on
  `Github <http://github.com/latestrevision/django-measurement/issues>`_.
- Test status available on
  `Travis-CI <https://travis-ci.org/latestrevision/django-measurement>`_.



.. image:: https://d2weczhvl823v0.cloudfront.net/latestrevision/django-measurement/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

