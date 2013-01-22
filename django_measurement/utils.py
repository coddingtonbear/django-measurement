import inspect

from django.conf import settings


MEASURE_OVERRIDES = getattr(settings, 'MEASURE_OVERRIDES', {})


def get_class_by_path(path):
    mod = __import__('.'.join(path.split('.')[:-1]))
    components = path.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def build_measure_list():
    from django.contrib.gis.measure import MeasureBase as DjangoMeasureBase
    from django_measurement.base import MeasureBase
    from django_measurement import measure
    measures = {}
    possible_measures = dir(measure)
    for possible_measure_name in possible_measures:
        possible_measure = getattr(measure, possible_measure_name)
        if not inspect.isclass(possible_measure):
            continue
        if issubclass(possible_measure, (MeasureBase, DjangoMeasureBase, )):
            measures[possible_measure_name] = possible_measure
    for overridden_measure_name, cls_path in MEASURE_OVERRIDES.items():
        cls = get_class_by_path(
            cls_path
        )
        measures[overridden_measure_name] = cls
    return measures


def get_measurement(measure, value, unit):
    return measure(
        **{unit: value}
    )
    

def guess_measurement(value, unit):
    all_measures = build_measure_list()
    for measure_name, measure in all_measures.items():
        all_units = getattr(measure, 'UNITS', {}).keys()
        if unit in all_units:
            return get_measurement(measure, value, unit)
