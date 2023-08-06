import copy

import six
from basicco import mangling, mapping_proxy, obj_state
from estruttura import ImmutableStructure, StructureMeta, UserImmutableStructure
from tippo import Any, Type, TypeVar

from ._attribute import Attribute
from ._bases import BaseData, BaseDataMeta, BasePrivateData

KT = TypeVar("KT")
VT = TypeVar("VT")


class DataMeta(StructureMeta, BaseDataMeta):
    """Metaclass for :class:`PrivateData`."""

    @staticmethod
    def __edit_dct__(this_attribute_map, attribute_map, name, bases, dct, **kwargs):  # noqa
        """
        Static method hook to edit the class dictionary.

        :param this_attribute_map: Attribute map for this class only.
        :param attribute_map: Attribute map with all attributes.
        :param name: Class name.
        :param bases: Class bases.
        :param dct: Class dictionary.
        :param kwargs: Class keyword arguments.
        :return: Edited class dictionary.
        """
        slots = list(dct.get("__slots__", ()))
        for attribute_name, attribute in six.iteritems(this_attribute_map):
            if attribute.constant:
                dct[attribute_name] = attribute.default
            else:
                slots.append(mangling.mangle(attribute_name, name))
                del dct[attribute_name]
        dct["__slots__"] = tuple(slots)
        return dct


class PrivateData(six.with_metaclass(DataMeta, BasePrivateData, ImmutableStructure)):
    """Private data."""

    __slots__ = ()

    __attribute_type__ = Attribute

    def __copy__(self):
        # type: (PD) -> PD
        """
        Make a shallow copy.

        :return: Shallow copy.
        """
        cls = type(self)
        new_self = cls.__new__(cls)
        obj_state.update_state(new_self, obj_state.get_state(self))
        return new_self

    def __getitem__(self, name):
        # type: (str) -> Any
        """
        Get value for attribute.

        :param name: Attribute name.
        :return: Attribute value.
        :raises KeyError: Attribute does not exist or has no value.
        """
        return getattr(self, name)

    def __contains__(self, name):
        # type: (object) -> bool
        """
        Get whether there's a value for attribute.

        :param name: Attribute name.
        :return: True if has value.
        """
        return isinstance(name, six.string_types) and name in type(self).__attribute_map__ and hasattr(self, name)

    def __setattr__(self, name, value):
        # type: (str, Any) -> None
        """
        Prevent setting attribute value.

        :param name: Attribute name.
        :param value: Attribute value.
        """
        if name in type(self).__attribute_map__:
            error = "{!r} objects are immutable".format(type(self).__name__)
            raise AttributeError(error)
        super(PrivateData, self).__setattr__(name, value)

    def __delattr__(self, name):
        # type: (str) -> None
        """
        Prevent deleting attribute value.

        :param name: Attribute name.
        """
        if name in type(self).__attribute_map__:
            error = "{!r} objects are immutable".format(type(self).__name__)
            raise AttributeError(error)
        super(PrivateData, self).__delattr__(name)

    def _do_init(self, initial_values):
        # type: (mapping_proxy.MappingProxyType[str, Any]) -> None
        """
        Initialize attribute values (internal).

        :param initial_values: Initial values.
        """
        for name, value in six.iteritems(initial_values):
            object.__setattr__(self, name, value)

    @classmethod
    def _do_deserialize(cls, values):
        # type: (Type[PD], mapping_proxy.MappingProxyType[str, Any]) -> PD
        """
        Deserialize (internal).

        :param values: Deserialized values.
        :return: Structure.
        :raises SerializationError: Error while deserializing.
        """
        self = cls.__new__(cls)
        self._do_init(values)
        return self


PD = TypeVar("PD", bound=PrivateData)  # private data self type


class Data(PrivateData, BaseData, UserImmutableStructure):
    """Data."""

    __slots__ = ()

    def _do_update(
        self,  # type: D
        inserts,  # type: mapping_proxy.MappingProxyType[str, Any]
        deletes,  # type: mapping_proxy.MappingProxyType[str, Any]
        updates_old,  # type: mapping_proxy.MappingProxyType[str, Any]
        updates_new,  # type: mapping_proxy.MappingProxyType[str, Any]
        updates_and_inserts,  # type: mapping_proxy.MappingProxyType[str, Any]
        all_updates,  # type: mapping_proxy.MappingProxyType[str, Any]
    ):
        # type: (...) -> D
        """
        Update attribute values (internal).

        :param inserts: Keys and values being inserted.
        :param deletes: Keys and values being deleted.
        :param updates_old: Keys and values being updated (old values).
        :param updates_new: Keys and values being updated (new values).
        :param updates_and_inserts: Keys and values being updated or inserted.
        :param all_updates: All updates.
        :return: Transformed (immutable) or self (mutable).
        """
        new_self = copy.copy(self)
        new_self._do_init(updates_and_inserts)
        for name, _ in six.iteritems(deletes):
            object.__delattr__(self, name)
        return new_self


D = TypeVar("D", bound=Data)  # data self type
