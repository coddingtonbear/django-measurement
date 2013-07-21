from django.conf import settings
from measurement.base import BidimensionalMeasure
from measurement.utils import get_all_measures, guess as guess_measurement

from django_measurement.measure import UnknownMeasure

MEASURE_OVERRIDES = getattr(settings, 'MEASURE_OVERRIDES', {})


def get_class_by_path(path):
    mod = __import__('.'.join(path.split('.')[:-1]))
    components = path.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def get_measure_unit_choices(include_measure=False):
    measures = build_measure_list()
    final_list = []
    for measure_name, measure in measures.items():
        if issubclass(measure, UnknownMeasure):
            continue
        if issubclass(measure, BidimensionalMeasure):
            continue
        measure_items = []
        for unit_name, _ in measure.UNITS.items():
            measure_items.append(
                ('%s.%s' % (measure_name, unit_name, ) if include_measure else unit_name, unit_name)
            )
        this_measure = tuple([measure_name, tuple(measure_items)])
        final_list.append(this_measure)
    return tuple(final_list)


def build_measure_list():
    all_measures = get_all_measures()
    measures = dict([(measure.__name__, measure) for measure in all_measures])
    for overridden_measure_name, cls_path in MEASURE_OVERRIDES.items():
        cls = get_class_by_path(
            cls_path
        )
        measures[overridden_measure_name] = cls
    # For unknown retrieved measures
    measures['UnknownMeasure'] = UnknownMeasure
    return measures


def get_measurement(measure, value, unit, original_unit=None):
    m = measure(
        **{unit: value}
    )
    if original_unit:
        m.unit = original_unit
    if isinstance(m, BidimensionalMeasure):
        m.reference.value = 1
    return m
