from __future__ import annotations

import inspect
from numbers import Number
from typing import Any, Dict, List, Type, Union, cast

import marshmallow
import marshmallow_dataclass
import marshmallow_oneofschema
import marshmallow_pyfields
import numpy as np
from marshmallow import Schema, fields, post_load
from pint import Unit

from optool.autocode import Attribute
from optool.logging import LOGGER
from optool.serialization.schemas import NumericField, QuantityField, UnitField
from optool.types import Quantity


class TypeRegister:
    _FIELDS = Schema.TYPE_MAPPING.copy()
    _FIELDS[Number] = NumericField
    _FIELDS[np.ndarray] = NumericField
    _FIELDS[Quantity] = QuantityField
    _FIELDS[Unit] = UnitField

    _SCHEMAS = {}  # type: Dict[type, Type[Schema]]

    @classmethod
    def contains(cls, class_or_obj: Union[Type[Any], Any]) -> bool:
        obj_type = cls._get_type(class_or_obj)
        return obj_type in cls._FIELDS and obj_type in cls._SCHEMAS

    @classmethod
    def add(cls, class_or_obj: Union[Type[Any], Any]) -> None:
        obj_type = cls._get_type(class_or_obj)
        if cls.contains(obj_type):
            return
        schema_type = cls.create_schema_using_fields(obj_type)
        cls.add_schema(schema_type, obj_type)

    @classmethod
    def add_schema(cls, schema_type: Type[Schema], obj_type: Type[Any]) -> None:
        if cls.contains(obj_type):
            return
        field_type = cls._make_field_type_for(schema_type, obj_type)
        cls._SCHEMAS[obj_type] = schema_type
        cls._FIELDS[obj_type] = field_type

    @classmethod
    def get_field_type(cls, obj_type: Type[Any]) -> Type[fields.Field]:
        cls._check_availability(obj_type, cls._FIELDS, "field")
        return cls._FIELDS[obj_type]

    @classmethod
    def get_schema_type(cls, obj_type: Type[Any]) -> Type[Schema]:
        cls._check_availability(obj_type, cls._SCHEMAS, "schema")
        return cls._SCHEMAS[obj_type]

    @classmethod
    def get_field(cls, class_or_obj: Union[Type[Any], Any], *args, **kwargs) -> fields.Field:
        obj_type = cls._get_type(class_or_obj)
        field_type = cls.get_field_type(obj_type)
        LOGGER.debug("Found field {} for type {}.", field_type.__name__, obj_type.__name__)
        try:
            return field_type(*args, **kwargs)
        except Exception as e:
            raise ValueError(f"Could not create field {field_type} with arguments {[args, kwargs]}") from e

    @classmethod
    def get_schema(cls, class_or_obj: Union[Type[Any], Any], *args, **kwargs) -> Schema:
        obj_type = cls._get_type(class_or_obj)
        schema_type = cls.get_schema_type(obj_type)
        LOGGER.debug("Found schema {} for type {}.", schema_type.__name__, obj_type.__name__)
        try:
            return schema_type(*args, **kwargs)
        except Exception as e:
            raise ValueError(f"Could not create schema {schema_type} with arguments {[args, kwargs]}") from e

    @staticmethod
    def _make_field_type_for(schema_type: Type[Schema], obj_type: Type[Any]) -> Type[fields.Field]:
        super_class = fields.Nested

        def field_type_init_func(self, *args, **kwargs):
            super_class.__init__(self, schema_type, *args, **kwargs)  # type:ignore

        field_type = type(f"{obj_type.__name__}Field", (super_class,), {"__init__": field_type_init_func})
        return cast(Type[fields.Field], field_type)

    @staticmethod
    def _check_availability(class_or_obj: Union[Type[Any], Any], options: Dict[type, Type[Any]], name: str) -> None:
        value_type = TypeRegister._get_type(class_or_obj)
        if value_type not in options:
            raise ValueError(f"There is no {name} specified for the type {value_type.__name__}. "
                             f"You may want to add the decorator @serializable to your class. "
                             f"Currently supported types are: {[k.__name__ for k in options]}")

    @staticmethod
    def _get_type(class_or_obj: Union[Type[Any], Any]) -> Type[Any]:
        return class_or_obj if inspect.isclass(class_or_obj) else type(class_or_obj)

    @classmethod
    def create_schema_using_fields(cls, obj_type: Type[Any]) -> Type[Schema]:
        schema_name = f"{obj_type.__name__}Schema"

        # noinspection PyShadowingNames
        fields = Attribute.reveal(obj_type)
        if len(fields) == 0:
            # noinspection PyUnusedLocal
            @post_load
            def create_object(self, data, **kwargs):
                return obj_type()

            return cast(Type[Schema], type(schema_name, (BaseSchema,), {"create_object": create_object}))

        # Copy all marshmallow hooks and whitelisted members of the dataclass to the schema.
        attributes = {
            k: v
            for k, v in inspect.getmembers(obj_type)
            if hasattr(v, "__marshmallow_hook__") or k in marshmallow_pyfields.main.MEMBERS_WHITELIST
        }

        # Update the schema members to contain marshmallow fields instead of dataclass fields
        for field in fields:
            field_name: str = field.name  # type: ignore
            attributes[field_name] = marshmallow_dataclass.field_for_schema(
                typ=field.serialize_as if field.serialize_as else field.type_hint,
                default=marshmallow.missing if field.is_mandatory else marshmallow_pyfields.main.get_default(field),
                metadata=None,  # type:ignore
                base_schema=BaseSchema)

        # noinspection PyProtectedMember
        schema_class = type(schema_name, (marshmallow_dataclass._base_schema(obj_type, BaseSchema),), attributes)
        return cast(Type[Schema], schema_class)


class BaseSchema(Schema):
    # noinspection PyProtectedMember
    TYPE_MAPPING = TypeRegister._FIELDS

    class Meta:
        ordered = True


# noinspection PyUnresolvedReferences
class PolymorphicSchema(marshmallow_oneofschema.OneOfSchema):
    type_field = "object_type"

    class Meta:
        ordered = True

    @property
    def type_schemas(self):
        """
        Dictionary of all known subtypes of this class implemented as name-to-Schema mapping to get schema for that
        particular object type.
        """
        # This is a hacky way of overloading the static field. As a result, the type_schema dict is not shared among all
        # classes that extend PolymorphicSchema, but we can get only the values we actually want. This is done by using
        # another static member called "known_types", which is, however, only present in the classes that extend
        # PolymorphicSchema. Hence, each of these classes has their own types. Important: All of this is only possible
        # since OneOfSchema uses internally self.type_schemas instead of cls.type_schemas, basically treating the value
        # as a member attribute and not a class attribute.
        return self.known_types

    @staticmethod
    def create_schema(obj_type: Type[Any]) -> Type[PolymorphicSchema]:
        schema_name = f'{obj_type.__name__}Schema'
        LOGGER.debug("Creating schema {} for polymorphism.", schema_name)
        return cast(Type[PolymorphicSchema], type(schema_name, (PolymorphicSchema,), {"known_types": {}}))

    @classmethod
    def get_known_types(cls) -> List[Type[Any]]:
        return list(cls.known_types.values())

    @classmethod
    def add_type(cls, obj_type: Type[Any]):
        LOGGER.info("Adding {} as type schema to {}.", obj_type.__name__, cls.__name__)
        cls.known_types[obj_type.__name__] = TypeRegister.get_schema_type(obj_type)
        LOGGER.debug("Now, for {} {} type schemas are present for the following classes: {}.", cls.__name__,
                     len(cls.known_types), list(cls.known_types.keys()))
