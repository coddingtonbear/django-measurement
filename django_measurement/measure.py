from django_measurement.base import Distance, Area, MeasureBase

__all__ = [
    'Distance',
    'Area',
    'Weight',
    'Volume',
]

class Weight(MeasureBase):
    STANDARD_UNIT = 'g'
    UNITS = {
        'mcg': 0.000001,
        'mg': 0.001,
        'g': 1.0,
        'kg': 1000.0,
        'tonne': 1000000.0,
        'oz': 28.3495,
        'lb': 453.592,
        'stone': 6350.29,
        'short_ton': 907185.0,
        'long_ton': 1016000.0,
    }
    ALIAS = {
        'microgram': 'mcg',
        'milligram': 'mg',
        'gram': 'g',
        'kilogram': 'kg',
        'ton': 'short_ton',
        'metric tonne': 'tonne',
        'metric ton': 'tonne',
        'ounce': 'oz',
        'pound': 'lb',
        'short ton': 'short_ton',
        'long ton': 'long_ton',
    }
    LALIAS = dict([(k.lower(), v) for k, v in ALIAS.items()])

class Volume(MeasureBase):
    STANDARD_UNIT = 'cubic_meter'
    UNITS = {
        'us_g': 0.00378541,
        'us_qt': 0.000946353,
        'us_pint': 0.000473176,
        'us_cup': 0.000236588,
        'us_oz': 2.9574e-5,
        'us_tbsp': 1.4787e-5,
        'us_tsp': 4.9289e-6,
        'cubic_centimeter': 100.0,
        'cubic_meter': 1.0,
        'l': 0.001,
        'ml': 1e-6,
        'cubic_foot': 0.0283168,
        'cubic_inch': 1.6387e-5,
        'imperial_g': 0.00454609,
        'imperial_qt': 0.00113652,
        'imperial_pint': 0.000568261,
        'imperial_oz': 2.8413e-5,
        'imperial_tbsp': 1.7758e-5,
        'imperial_tsp': 5.9194e-6,
    }
    ALIAS = {
        'US Gallon': 'us_g',
        'US Quart': 'us_qt',
        'US Pint': 'us_pint',
        'US Cup': 'us_cup',
        'US Ounce': 'us_oz',
        'US Fluid Ounce': 'us_oz',
        'US Tablespoon': 'us_tbsp',
        'US Teaspoon': 'us_tsp',
        'cubic centimeter': 'cubic_centimeter',
        'cubic meter': 'cubic_meter',
        'liter': 'l',
        'milliliter': 'ml',
        'cubic foot': 'cubic_foot',
        'cubic inch': 'cubic_inch',
        'Imperial Gram': 'imperial_g',
        'Imperial Quart': 'imperial_qt',
        'Imperial Pint': 'imperial_pint',
        'Imperial Ounce': 'imperial_oz',
        'Imperial Tablespoon': 'imperial_tbsp',
        'Imperial Teaspoon': 'imperial_tsp',
    }
    LALIAS = dict([(k.lower(), v) for k, v in ALIAS.items()])

    def __init__(self, *args, **kwargs):
        super(Volume, self).__init__(*args, **kwargs)

