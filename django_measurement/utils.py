import decimal
from typing import Type

from measurement.base import AbstractMeasure


def get_measurement(
    measure: Type[AbstractMeasure], value: decimal.Decimal
) -> AbstractMeasure:
    unit = next(iter(measure._units.keys()))
    return measure(f"{value} {unit}")
