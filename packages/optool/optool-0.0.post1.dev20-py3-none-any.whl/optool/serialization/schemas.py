from numbers import Number

import marshmallow
import numpy as np
from marshmallow import Schema, fields, post_load
from pint.util import to_units_container

from optool.logging import LOGGER
from optool.types import UNITS, Quantity


class NumericField(fields.Field):
    """
    A :py:class:`~marshmallow.fields.Field` which allows to keep the type of any dimensionless numeric type such as
    :py:class:`~numbers.Number` or :py:class:`~numpy.ndarray` throughout serialization and deserialization.

    See Also: :py:data:`~optool.util.types.DIMENSIONLESS_TYPES`
    """

    def _serialize(self, value, attr, obj, **kwargs):
        LOGGER.debug("Serializing: {}", value)
        if value is None:
            return None
        elif isinstance(value, np.floating):
            return {"type": f"np.{type(value).__name__}", "value": str(value)}
        elif isinstance(value, Number):
            return {"type": type(value).__name__, "value": str(value)}
        elif isinstance(value, np.ndarray):
            return {"type": "ndarray", "value": value.tolist()}
        else:
            raise marshmallow.ValidationError(f"Cannot serialize values of type: {type(value)}.")

    def _deserialize(self, value, attr, data, **kwargs):
        LOGGER.debug("Deserializing: {}", value)
        if value is None:
            return None

        try:
            if value["type"] == "ndarray":
                return np.array(value["value"])

            creator = f"{value['type']}('{value['value']}')"
            LOGGER.debug("Trying to create the number with \"{}\".", creator)
            number = eval(creator)
            LOGGER.debug("The result is: {}", number)
            if not isinstance(number, Number):
                raise marshmallow.ValidationError(f"Cannot deserialize values of type: {type(number)}.")
            return number
        except Exception as error:
            raise marshmallow.ValidationError(f"Unknown value received: {value}.") from error


class UnitField(fields.Field):
    """
    A :py:class:`~marshmallow.fields.Field` to serialize and deserialize :py:class:`~pint.Unit` objects.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        LOGGER.debug("Serializing: {}", value)
        return None if value is None else dict(to_units_container(value))

    def _deserialize(self, value, attr, data, **kwargs):
        LOGGER.debug("Deserializing: {}", value)
        return None if value is None else UNITS.Unit(UNITS.UnitsContainer(value))


class QuantitySchema(Schema):
    """
    A :py:class:`~marshmallow.Schema` to serialize and deserialize quantities created via
    :py:class:`~optool.util.types.Quantity`.
    """

    magnitude = NumericField(allow_none=True)
    units = UnitField(allow_none=True)

    class Meta:
        ordered = True

    # noinspection PyUnusedLocal
    @post_load
    def create_object(self, data, **kwargs):
        LOGGER.debug("Creating quantity object from: {}, which is of type {}", data, type(data))
        return Quantity(data["magnitude"], data["units"])


class QuantityField(fields.Nested):
    """
    A :py:class:`~marshmallow.fields.Field` to serialize and deserialize quantities created via
    :py:class:`~optool.util.types.Quantity`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(QuantitySchema, *args, **kwargs)  # type:ignore
