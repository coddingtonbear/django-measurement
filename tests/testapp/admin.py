from django.contrib import admin

from . import models


@admin.register(models.MeasurementTestModel)
class MeasurementTestModelAdmin(admin.ModelAdmin):
    pass
