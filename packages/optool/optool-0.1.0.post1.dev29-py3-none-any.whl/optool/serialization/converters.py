import pickle
import uuid
from abc import ABC
from hashlib import sha1
from itertools import chain
from traceback import TracebackException
from typing import Generic, Type, TypeVar, Union

import marshmallow.fields
from marshmallow import Schema

from optool.serialization.registry import PolymorphicSchema, TypeRegister

T = TypeVar("T")


class Serializer(Generic[T]):
    __slots__ = '_schema', '_obj'

    def __init__(self, obj: T):
        self._schema = TypeRegister.get_schema(obj)
        self._obj = obj

    def to_dict(self) -> dict:
        return self._schema.dump(self._obj)

    def to_json(self) -> str:
        return self._schema.dumps(self._obj)


class Deserializer(Generic[T]):
    __slots__ = '_schema', '_type'

    def __init__(self, obj_type: Type[T]):
        self._schema = TypeRegister.get_schema(obj_type)
        self._type = obj_type

    def from_dict(self, raw: dict) -> T:
        try:
            errors = self._schema.validate(raw)
        except Exception as e:
            trace = TracebackException.from_exception(e)
            file_name = trace.stack[-1].filename
            if str(e) != "not all arguments converted during string formatting" or "one_of_schema" not in file_name:
                raise

            supported_polymorphism = {}
            for field_name, field in self._schema.fields.items():
                if isinstance(field, marshmallow.fields.Nested):
                    nested_schema: Type[Schema] = field.nested  # type: ignore
                    if issubclass(nested_schema, PolymorphicSchema):
                        supported_types = nested_schema.get_known_types()
                        supported_polymorphism[nested_schema.__name__] = [type.__name__ for type in supported_types]

            raise ValueError(f"Was not able to deserialize object of type {self._type.__name__!r}. "
                             f"From the error message, we guess that there is a missing type for polymorphism. "
                             f"Check in the following list if this might be the case. "
                             f"Currently supported polymorphism:\n{supported_polymorphism}") from e

        error_values_flat = list(chain(*errors.values()))
        basic_err_msg = f"Cannot deserialize the dictionary to {self._type.__name__}"
        if "Unknown field." in error_values_flat:
            raise ValueError(f"{basic_err_msg} most likely because the dictionary does not match the class definition, "
                             f"see the following issues reported:\n{errors}")
        elif len(errors) > 0:
            raise ValueError(f"{basic_err_msg} due to the following issues:\n{errors}")
        return self._schema.load(raw)

    def from_json(self, raw: str) -> T:
        return self._schema.loads(raw)


class UuidGenerator:
    __slots__ = '_uuid'

    def __init__(self, obj):
        sha = sha1(uuid.NAMESPACE_URL.bytes + pickle.dumps(obj)).digest()
        self._uuid = uuid.UUID(bytes=sha[:16], version=5)

    def get_uuid(self):
        return self._uuid

    def get_hex(self):
        return self._uuid.hex


class JsonConvertible(ABC):
    """
    A utility class which offers convenient methods to convert the object to JSON and vice versa.
    """

    def to_dict(self) -> dict:
        """
        Serializes the object recursively to a dictionary of only dictionaries and basic types.
        """
        return Serializer(self).to_dict()

    def to_json(self) -> str:
        """
        Serializes the object to a JSON string.
        """
        return Serializer(self).to_json()

    @classmethod
    def from_json(cls, dict_or_str: Union[dict, str]):
        """
        Deserializes an object from a dictionary or a JSON string.
        """
        if isinstance(dict_or_str, str):
            return Deserializer(cls).from_json(dict_or_str)
        return Deserializer(cls).from_dict(dict_or_str)


class BinaryConvertible(ABC):
    """
    A utility class which offers convenient methods to convert the object to byte stream and vice versa.
    """

    def to_blob(self) -> bytes:
        """
        Serializes the object to a byte stream.
        """
        return pickle.dumps(self)

    def get_uuid(self) -> uuid.UUID:
        """
        Create a universally unique identifier.
        """

        if isinstance(self, JsonConvertible):
            # Since result of to_blob() is always changing, we use the generation of dict via marshmallow.
            # However, this requires that all schemas to have a metaclass that tells them to order the fields.
            return UuidGenerator(self.to_dict()).get_uuid()

        return UuidGenerator(self).get_uuid()

    @classmethod
    def from_blob(cls, blob: bytes):
        """
        Deserializes an object from a byte stream.
        """
        return pickle.loads(blob)
