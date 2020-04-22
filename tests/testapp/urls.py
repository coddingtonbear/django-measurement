from django.urls import path, include
from django.views import generic
from django.contrib import admin

from . import models

urlpatterns = [
    path(
        "",
        generic.CreateView.as_view(
            model=models.MeasurementTestModel, fields="__all__", success_url="/"
        ),
    ),
    path('admin/', admin.site.urls)
]
