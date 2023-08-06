import copy

from estruttura import ImmutableSetStructure, UserImmutableSetStructure
from pyrsistent import pset
from pyrsistent.typing import PSet
from tippo import AbstractSet, Iterable, Iterator, Type, TypeVar

from ._bases import DataCollection, PrivateDataCollection

T = TypeVar("T")


class PrivateSetData(PrivateDataCollection[T], ImmutableSetStructure[T]):
    """Private set data."""

    __slots__ = ("_state",)

    def __iter__(self):
        # type: () -> Iterator[T]
        """
        Iterate over values.

        :return: Value iterator.
        """
        return iter(self._state)

    def __len__(self):
        # type: () -> int
        """
        Get value count.

        :return: Value count.
        """
        return len(self._state)

    def __contains__(self, value):
        # type: (object) -> bool
        """
        Get whether contains value or not.

        :param value: Value.
        :return: True if contains.
        """
        return value in self._state

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
        # type: (frozenset[T]) -> None
        """
        Initialize values (internal).

        :param initial_values: New values.
        """
        self._state = pset(initial_values)  # type: PSet[T]

    @classmethod
    def _do_deserialize(cls, values):
        # type: (Type[PSD], frozenset[T]) -> PSD
        """
        Deserialize (internal).

        :param values: Deserialized values.
        :return: List structure.
        :raises SerializationError: Error while deserializing.
        """
        self = cls.__new__(cls)
        self._state = pset(values)
        return self

    def isdisjoint(self, iterable):
        # type: (Iterable) -> bool
        """
        Get whether is a disjoint set of an iterable.

        :param iterable: Iterable.
        :return: True if is disjoint.
        """
        return self._state.isdisjoint(iterable)

    def issubset(self, iterable):
        # type: (Iterable) -> bool
        """
        Get whether is a subset of an iterable.

        :param iterable: Iterable.
        :return: True if is subset.
        """
        return self._state.issubset(iterable)

    def issuperset(self, iterable):
        # type: (Iterable) -> bool
        """
        Get whether is a superset of an iterable.

        :param iterable: Iterable.
        :return: True if is superset.
        """
        return self._state.issuperset(iterable)

    def intersection(self, iterable):
        # type: (Iterable) -> AbstractSet
        """
        Get intersection.

        :param iterable: Iterable.
        :return: Intersection.
        """
        return self._state.intersection(iterable)

    def symmetric_difference(self, iterable):
        # type: (Iterable) -> AbstractSet
        """
        Get symmetric difference.

        :param iterable: Iterable.
        :return: Symmetric difference.
        """
        return self._state.symmetric_difference(iterable)

    def union(self, iterable):
        # type: (Iterable) -> AbstractSet
        """
        Get union.

        :param iterable: Iterable.
        :return: Union.
        """
        return self._state.union(iterable)

    def difference(self, iterable):
        # type: (Iterable) -> AbstractSet
        """
        Get difference.

        :param iterable: Iterable.
        :return: Difference.
        """
        return self._state.difference(iterable)

    def inverse_difference(self, iterable):
        # type: (Iterable) -> AbstractSet
        """
        Get an iterable's difference to this.

        :param iterable: Iterable.
        :return: Inverse Difference.
        """
        return pset(iterable).difference(self._state)


PSD = TypeVar("PSD", bound=PrivateSetData)  # private set data self type


class SetData(PrivateSetData[T], DataCollection[T], UserImmutableSetStructure[T]):
    """Set data."""

    __slots__ = ()

    def _do_remove(self, old_values):
        # type: (SD, frozenset[T]) -> SD
        """
        Remove values (internal).

        :param old_values: Old values.
        :return: Transformed (immutable) or self (mutable).
        """
        new_state = self._state.difference(old_values)
        new_self = copy.copy(self)
        new_self._state = new_state
        return new_self

    def _do_update(self, new_values):
        # type: (SD, frozenset[T]) -> SD
        """
        Add values (internal).

        :param new_values: New values.
        :return: Transformed (immutable) or self (mutable).
        """
        new_state = self._state.update(new_values)
        new_self = copy.copy(self)
        new_self._state = new_state
        return new_self


SD = TypeVar("SD", bound=SetData)  # set data self type
