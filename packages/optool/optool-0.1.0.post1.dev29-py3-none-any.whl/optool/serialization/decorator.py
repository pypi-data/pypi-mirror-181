from typing import Any, Optional, Type

from optool.serialization.registry import PolymorphicSchema, TypeRegister


def serializable(cls: Optional[Type[Any]] = None, /, *, only_subclasses: bool = False):
    """
    A decorator to enable serialization via :py:mod:`marshmallow`.

    Args:
        only_subclasses (bool): allow polymorphism

    Returns: a decorator for classes
    """

    # noinspection PyShadowingNames
    def wrap(cls):

        if only_subclasses:
            schema_class = PolymorphicSchema.create_schema(cls)
            TypeRegister.add_schema(schema_class, cls)  # type:ignore

        else:
            TypeRegister.add(cls)

            for parent_class in cls.mro()[1:]:
                if TypeRegister.contains(parent_class):
                    parent_schema_class = TypeRegister.get_schema_type(parent_class)
                    if issubclass(parent_schema_class, PolymorphicSchema):
                        parent_schema_class.add_type(cls)

        return cls

    # See if we're being called with or without parentheses
    if cls is None:
        # We're called with parentheses
        return wrap

    # We're called without parentheses
    return wrap(cls)
