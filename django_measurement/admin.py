import re

import django
from django import forms
from django.contrib.admin import ModelAdmin
from django.contrib import messages

from django_measurement.fields import MeasurementValueField
from django_measurement.utils import build_measure_list, guess_measurement


all_measures = build_measure_list()


class MeasurementAdminForm(forms.ModelForm):
    MEASURE_FIELD_NAME_RE = re.compile('^(.*)_value$')
    MEASURE_VALUE_SPLIT_RE = re.compile('^([0-9.-]+) ([a-zA-Z_/]+)$')
    MEASURE_FIELDS = {}

    def __init__(self, *args, **kwargs):
        self.MEASURE_FIELDS = {}
        instance = None
        if 'instance' in kwargs:
            instance = kwargs['instance']
        super(MeasurementAdminForm, self).__init__(*args, **kwargs)
        for field in self.Meta.model._meta.fields:
            if isinstance(field, MeasurementValueField):
                attr_name = self.MEASURE_FIELD_NAME_RE.match(
                    field.name
                ).group(1)
                self.MEASURE_FIELDS[attr_name] = {
                    'required': not field.blank
                }
        for field, fkwargs in self.MEASURE_FIELDS.items():
            choices = [(k, k) for k in all_measures.keys()]
            choices.insert(0, (None, ''))
            self.fields[field + '_measure'] = forms.ChoiceField(
                choices=choices,
                **fkwargs
            )
            self.fields[field] = forms.CharField(**fkwargs)
            if instance is not None:
                value = getattr(instance, field)
                self.initial[field + '_measure'] = value.__class__.__name__
                self.initial[field] = str(value)

    def clean(self):
        for field in self.MEASURE_FIELDS.keys():
            if field + '_measure' not in self.cleaned_data:
                continue
            measure_name = self.cleaned_data[field + '_measure']
            measure_value = self.cleaned_data.get(field, '')

            if not measure_value or not measure_name:
                continue

            measure = all_measures[measure_name]
            matcher = self.MEASURE_VALUE_SPLIT_RE.match(measure_value)
            try:
                unit = matcher.group(2).replace('/', '__')
                measurement = guess_measurement(
                    matcher.group(1), unit,
                    measures=[measure]
                )
            except (ValueError, AttributeError):
                raise forms.ValidationError(
                    '%s is not a valid measurement of %s' % (
                        measure_value,
                        measure_name.lower(),
                    )
                )
            self.cleaned_data.pop(field + '_measure')
            self.cleaned_data[field] = measurement
        return self.cleaned_data

    def save(self, *args, **kwargs):
        for field in self.MEASURE_FIELDS:
            setattr(
                self.instance,
                field,
                self.cleaned_data[field]
            )
        return super(MeasurementAdminForm, self).save(*args, **kwargs)


class MeasurementAdmin(ModelAdmin):
    form = MeasurementAdminForm

    def get_fieldsets(self, request, obj=None):
        if django.VERSION[0:2] >= (1, 6):
            messages.add_message(
                request,
                messages.WARNING,
                "django-measurements is currently not able to display "
                "measurement fields for Django versions above 1.5. "
                "See https://github.com/latestrevision"
                "/django-measurement/issues/3 "
                "for more information.",
                fail_silently=True
            )
        else:
            form = self.get_form(request, obj)(instance=obj)
            return [(None, {'fields': form.fields.keys()})]
        return super(MeasurementAdmin, self).get_fieldsets(request, obj)
