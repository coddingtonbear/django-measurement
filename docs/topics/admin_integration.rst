
Admin Integration
=================

To enable admin integration such that you can edit your measurements in the
Django Admin, subclass the ``django_measurement.admin.MeasurementAdmin`` class
when creating your ``ModelAdmin`` in your app's ``admin.py``.

.. code-block:: python

   from django_measurement.admin import MeasurementAdmin
   from yourapp.models import YourModel

   class YourModelAdmin(MeasurementAdmin):
       pass

    admin.site.register(YourModel, YourModelAdmin)
