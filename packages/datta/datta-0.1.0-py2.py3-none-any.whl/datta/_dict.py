import copy

from basicco import mapping_proxy
from estruttura import ImmutableDictStructure, UserImmutableDictStructure
from pyrsistent import pmap
from pyrsistent.typing import PMap
from tippo import Iterator, Type, TypeVar

from ._bases import DataCollection, PrivateDataCollection
from ._constants import DeletedType

KT = TypeVar("KT")
VT = TypeVar("VT")


class PrivateDictData(PrivateDataCollection[KT], ImmutableDictStructure[KT, VT]):
    """Private dictionary data."""

    __slots__ = ("_state",)

    def __iter__(self):
        # type: () -> Iterator[KT]
        """
        Iterate over keys.

        :return: Keys iterator.
        """
        for key in self._state:
            yield key

    def __len__(self):
        # type: () -> int
        """
        Get key count.

        :return: Key count.
        """
        return len(self._state)

    def __getitem__(self, key):
        # type: (KT) -> VT
        """
        Get value for key.

        :param key: Key.
        :return: Value.
        """
        return self._state[key]

    def _hash(self):
        # type: () -> int
        """
        Get hash.

        :return: Hash.
        """
        return hash(self._state)

    def _eq(self, other):
        # type: (object) -> bool
        """
        Compare for equality.

        :param other: Another object.
        :return: True if equal.
        """
        if isinstance(other, dict):
            return self._state == other
        else:
            return isinstance(other, type(self)) and self._state == other._state

    def _do_init(self, initial_values):
        # type: (mapping_proxy.MappingProxyType[KT, VT]) -> None
        """
        Initialize keys and values (internal).

        :param initial_values: Initial values.
        """
        self._state = pmap(initial_values)  # type: PMap[KT, VT]

    @classmethod
    def _do_deserialize(cls, values):
        # type: (Type[PDD], mapping_proxy.MappingProxyType[KT, VT]) -> PDD
        """
        Deserialize (internal).

        :param values: Deserialized values.
        :return: Dictionary structure.
        :raises SerializationError: Error while deserializing.
        """
        self = cls.__new__(cls)
        self._state = pmap(values)
        return self


PDD = TypeVar("PDD", bound=PrivateDictData)  # private dictionary data self type


class DictData(PrivateDictData[KT, VT], DataCollection[KT], UserImmutableDictStructure[KT, VT]):
    """Dictionary data."""

    __slots__ = ()

    def _do_update(
        self,  # type: DD
        inserts,  # type: mapping_proxy.MappingProxyType[KT, VT]
        deletes,  # type: mapping_proxy.MappingProxyType[KT, VT]
        updates_old,  # type: mapping_proxy.MappingProxyType[KT, VT]
        updates_new,  # type: mapping_proxy.MappingProxyType[KT, VT]
        updates_and_inserts,  # type: mapping_proxy.MappingProxyType[KT, VT]
        all_updates,  # type: mapping_proxy.MappingProxyType[KT, VT | DeletedType]
    ):
        # type: (...) -> DD
        """
        Update keys and values (internal).

        :param inserts: Keys and values being inserted.
        :param deletes: Keys and values being deleted.
        :param updates_old: Keys and values being updated (old values).
        :param updates_new: Keys and values being updated (new values).
        :param updates_and_inserts: Keys and values being updated or inserted.
        :return: Transformed (immutable) or self (mutable).
        """
        new_state = self._state.update(updates_and_inserts)
        if deletes:
            new_state_evolver = new_state.evolver()
            for key in deletes:
                del new_state_evolver[key]
            new_state = new_state_evolver.persistent()
        new_self = copy.copy(self)
        new_self._state = new_state
        return new_self


DD = TypeVar("DD", bound=DictData)  # dictionary data self type
