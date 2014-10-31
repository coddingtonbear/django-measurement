.. image:: https://travis-ci.org/coddingtonbear/django-measurement.png?branch=master
   :target: https://travis-ci.org/coddingtonbear/django-measurement
.. image:: https://pypip.in/v/django-measurement/badge.png
  :target: https://crate.io/packages/django-measurement
.. image:: https://pypip.in/d/django-measurement/badge.png
  :target: https://crate.io/packages/django-measurement
.. image:: https://pypip.in/license/django-measurement/badge.png
  :target: https://pypi.python.org/pypi/django-measurement/

Easily use, manipulate, and store unit-aware measurement objects using Python
and Django.

**Note**: Currently, this is only compatible with Django 1.6 or later.

`django.contrib.gis.measure <https://github.com/django/django/blob/master/django/contrib/gis/measure.py>`_
has these wonderful 'Distance' objects that can be used not only for storing a
unit-aware distance measurement, but also for converting between different
units and adding/subtracting these objects from one another.

This module provides for a django model field and admin interface for storing
any measurements provided by `python-measurement <https://github.com/coddingtonbear/python-measurement>`_.

Example use with a model:

.. code-block:: python

   from django_measurement.fields import MeasurementField
   from django_measurement.measure import Volume
   from django.db import models
   
   class BeerConsumptionLogEntry(models.Model):
       name = models.CharField(max_length=255)
       volume = MeasurementField(measurement=Volume)
   
       def __unicode__(self):
           return u"%s of %s" % (self.name, self.volume)

   entry = BeerConsumptionLogEntry()
   entry.name = 'Bear Republic Racer 5'
   entry.volume = Volume(us_pint=1)
   entry.save()

These stored measurement objects can be used in all of the usual ways supported
by `python-measurement <https://github.com/coddingtonbear/python-measurement>`_
too:

.. code-block:: python

   >>> from django_measurement.measures import Weight
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
  `Github <http://github.com/coddingtonbear/django-measurement/issues>`_.
- Test status available on
  `Travis-CI <https://travis-ci.org/coddingtonbear/django-measurement>`_.

