|version| |ci| |coverage| |license|

Django Measurement
==================

Easily use, manipulate, and store unit-aware measurement objects using Python
and Django.

`django.contrib.gis.measure <https://github.com/django/django/blob/master/django/contrib/gis/measure.py>`_
has these wonderful 'Distance' objects that can be used not only for storing a
unit-aware distance measurement, but also for converting between different
units and adding/subtracting these objects from one another.

This module provides for a django model field and admin interface for storing
any measurements provided by `python-measurement`_.

Example use with a model:

.. code-block:: python

   from django_measurement.models import MeasurementField
   from measurement.measures import Volume
   from django.db import models
   
   class BeerConsumptionLogEntry(models.Model):
       name = models.CharField(max_length=255)
       volume = MeasurementField(measurement=Volume)
   
       def __str__(self):
           return f"{self.name} of {self.volume}"

   entry = BeerConsumptionLogEntry()
   entry.name = "Bear Republic Racer 5"
   entry.volume = Volume(us_pint=1)
   entry.save()

These stored measurement objects can be used in all of the usual ways supported
by `python-measurement`_
too:

.. code-block:: python

   >>> from measurement.measures import Mass
   >>> weight_1 = Mass(lb=125)
   >>> weight_2 = Mass(kg=40)
   >>> added_together = weight_1 + weight_2
   >>> added_together
   Mass(lb=213.18497680735112)
   >>> added_together.kg  # Maybe I actually need this value in kg?
   96.699

- Documentation for django-measurement is available via `Read the Docs`_.
- Please post issues on GitHub_.

.. _Read the Docs: https://django-measurement.readthedocs.io/
.. _GitHub: https://github.com/coddingtonbear/django-measurement/issues
.. _python-measurement: https://github.com/coddingtonbear/python-measurement

.. |version| image:: https://img.shields.io/pypi/v/django-measurement.svg
    :target: https://pypi.python.org/pypi/django-measurement
.. |ci| image:: https://api.travis-ci.org/coddingtonbear/django-measurement.svg?branch=master
    :target: https://travis-ci.org/coddingtonbear/django-measurement
.. |coverage| image:: https://codecov.io/gh/coddingtonbear/django-measurement/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/coddingtonbear/django-measurement
.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: LICENSE