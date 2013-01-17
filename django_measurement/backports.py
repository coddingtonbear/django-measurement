from decimal import Decimal

from django.utils import six

NUMERIC_TYPES = six.integer_types + (float, Decimal)

try:
    from functools import total_ordering
except ImportError:
    def total_ordering(cls):
        """Class decorator that fills in missing ordering methods"""
        convert = {
            '__lt__': [('__gt__', lambda self, other: not (self < other or self == other)),
                       ('__le__', lambda self, other: self < other or self == other),
                       ('__ge__', lambda self, other: not self < other)],
            '__le__': [('__ge__', lambda self, other: not self <= other or self == other),
                       ('__lt__', lambda self, other: self <= other and not self == other),
                       ('__gt__', lambda self, other: not self <= other)],
            '__gt__': [('__lt__', lambda self, other: not (self > other or self == other)),
                       ('__ge__', lambda self, other: self > other or self == other),
                       ('__le__', lambda self, other: not self > other)],
            '__ge__': [('__le__', lambda self, other: (not self >= other) or self == other),
                       ('__gt__', lambda self, other: self >= other and not self == other),
                       ('__lt__', lambda self, other: not self >= other)]
        }
        roots = set(dir(cls)) & set(convert)
        if not roots:
            raise ValueError('must define at least one ordering operation: < > <= >=')
        root = max(roots)       # prefer __lt__ to __le__ to __gt__ to __ge__
        for opname, opfunc in convert[root]:
            if opname not in roots:
                opfunc.__name__ = opname
                opfunc.__doc__ = getattr(int, opname).__doc__
                setattr(cls, opname, opfunc)
        return cls

def pretty_name(obj):
    return obj.__name__ if obj.__class__ == type else obj.__class__.__name__

@total_ordering
class MeasureBase(object):
    STANDARD_UNIT = None
    ALIAS  = {}
    UNITS  = {}
    LALIAS = {}

    def __init__(self, default_unit=None, **kwargs):
        value, self._default_unit = self.default_units(kwargs)
        setattr(self, self.STANDARD_UNIT, value)
        if default_unit and isinstance(default_unit, six.string_types):
            self._default_unit = default_unit

    def _get_standard(self):
        return getattr(self, self.STANDARD_UNIT)

    def _set_standard(self, value):
        setattr(self, self.STANDARD_UNIT, value)

    standard = property(_get_standard, _set_standard)

    def __getattr__(self, name):
        if name in self.UNITS:
            return self.standard / self.UNITS[name]
        else:
            raise AttributeError('Unknown unit type: %s' % name)

    def __repr__(self):
        return '%s(%s=%s)' % (pretty_name(self), self._default_unit,
            getattr(self, self._default_unit))

    def __str__(self):
        return '%s %s' % (getattr(self, self._default_unit), self._default_unit)

    # **** Comparison methods ****

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.standard == other.standard
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.standard < other.standard
        else:
            return NotImplemented

    # **** Operators methods ****

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(default_unit=self._default_unit,
                **{self.STANDARD_UNIT: (self.standard + other.standard)})
        else:
            raise TypeError('%(class)s must be added with %(class)s' % {"class":pretty_name(self)})

    def __iadd__(self, other):
        if isinstance(other, self.__class__):
            self.standard += other.standard
            return self
        else:
            raise TypeError('%(class)s must be added with %(class)s' % {"class":pretty_name(self)})

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(default_unit=self._default_unit,
                **{self.STANDARD_UNIT: (self.standard - other.standard)})
        else:
            raise TypeError('%(class)s must be subtracted from %(class)s' % {"class":pretty_name(self)})

    def __isub__(self, other):
        if isinstance(other, self.__class__):
            self.standard -= other.standard
            return self
        else:
            raise TypeError('%(class)s must be subtracted from %(class)s' % {"class":pretty_name(self)})

    def __mul__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            return self.__class__(default_unit=self._default_unit,
                **{self.STANDARD_UNIT: (self.standard * other)})
        else:
            raise TypeError('%(class)s must be multiplied with number' % {"class":pretty_name(self)})

    def __imul__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            self.standard *= float(other)
            return self
        else:
            raise TypeError('%(class)s must be multiplied with number' % {"class":pretty_name(self)})

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return self.standard / other.standard
        if isinstance(other, NUMERIC_TYPES):
            return self.__class__(default_unit=self._default_unit,
                **{self.STANDARD_UNIT: (self.standard / other)})
        else:
            raise TypeError('%(class)s must be divided with number or %(class)s' % {"class":pretty_name(self)})

    def __div__(self, other):   # Python 2 compatibility
        return type(self).__truediv__(self, other)

    def __itruediv__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            self.standard /= float(other)
            return self
        else:
            raise TypeError('%(class)s must be divided with number' % {"class":pretty_name(self)})

    def __idiv__(self, other):  # Python 2 compatibility
        return type(self).__itruediv__(self, other)

    def __bool__(self):
        return bool(self.standard)

    def __nonzero__(self):      # Python 2 compatibility
        return type(self).__bool__(self)

    def default_units(self, kwargs):
        """
        Return the unit value and the default units specified
        from the given keyword arguments dictionary.
        """
        val = 0.0
        default_unit = self.STANDARD_UNIT
        for unit, value in six.iteritems(kwargs):
            if not isinstance(value, float): value = float(value)
            if unit in self.UNITS:
                val += self.UNITS[unit] * value
                default_unit = unit
            elif unit in self.ALIAS:
                u = self.ALIAS[unit]
                val += self.UNITS[u] * value
                default_unit = u
            else:
                lower = unit.lower()
                if lower in self.UNITS:
                    val += self.UNITS[lower] * value
                    default_unit = lower
                elif lower in self.LALIAS:
                    u = self.LALIAS[lower]
                    val += self.UNITS[u] * value
                    default_unit = u
                else:
                    raise AttributeError('Unknown unit type: %s' % unit)
        return val, default_unit

    @classmethod
    def unit_attname(cls, unit_str):
        """
        Retrieves the unit attribute name for the given unit string.
        For example, if the given unit string is 'metre', 'm' would be returned.
        An exception is raised if an attribute cannot be found.
        """
        lower = unit_str.lower()
        if unit_str in cls.UNITS:
            return unit_str
        elif lower in cls.UNITS:
            return lower
        elif lower in cls.LALIAS:
            return cls.LALIAS[lower]
        else:
            raise Exception('Could not find a unit keyword associated with "%s"' % unit_str)


