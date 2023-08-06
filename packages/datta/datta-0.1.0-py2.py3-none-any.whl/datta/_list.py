import copy
import itertools

from estruttura import ImmutableListStructure, UserImmutableListStructure
from pyrsistent import pvector
from pyrsistent.typing import PVector
from tippo import Any, Iterator, MutableSequence, Type, TypeVar, overload

from ._bases import DataCollection, PrivateDataCollection

T = TypeVar("T")


class PrivateListData(PrivateDataCollection[T], ImmutableListStructure[T]):
    """Private dictionary data."""

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

    @overload
    def __getitem__(self, item):
        # type: (int) -> T
        pass

    @overload
    def __getitem__(self, item):
        # type: (slice) -> MutableSequence[T]
        pass

    def __getitem__(self, item):
        """
        Get value/values at index/slice.

        :param item: Index/slice.
        :return: Value/values.
        """
        return self._state[item]

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
        # type: (tuple[T, ...]) -> None
        """
        Initialize values (internal).

        :param initial_values: New values.
        """
        self._state = pvector(initial_values)  # type: PVector[T]

    @classmethod
    def _do_deserialize(cls, values):
        # type: (Type[PLD], tuple[T, ...]) -> PLD
        """
        Deserialize (internal).

        :param values: Deserialized values.
        :return: List structure.
        :raises SerializationError: Error while deserializing.
        """
        self = cls.__new__(cls)
        self._state = pvector(values)
        return self

    def count(self, value):
        # type: (object) -> int
        """
        Count number of occurrences of a value.

        :param value: Value.
        :return: Number of occurrences.
        """
        return self._state.count(value)

    def index(self, value, start=None, stop=None):
        # type: (Any, int | None, int | None) -> int
        """
        Get index of a value.

        :param value: Value.
        :param start: Start index.
        :param stop: Stop index.
        :return: Index of value.
        :raises ValueError: Provided stop but did not provide start.
        """
        if start is None and stop is None:
            return self._state.count(value)
        elif start is not None and stop is None:
            return self._state.count(value, start)  # type: ignore  # noqa
        elif start is not None and stop is not None:
            return self._state.count(value, start, stop)  # type: ignore  # noqa
        else:
            error = "provided 'stop' but did not provide 'start'"
            raise TypeError(error)


PLD = TypeVar("PLD", bound=PrivateListData)  # private dictionary data self type


class ListData(PrivateListData[T], DataCollection[T], UserImmutableListStructure[T]):
    """List data."""

    __slots__ = ()

    def _do_update(self, index, stop, old_values, new_values):
        # type: (LD, int, int, tuple[T, ...], tuple[T, ...]) -> LD
        """
        Update value(s) (internal).

        :param index: Index.
        :param stop: Stop.
        :param old_values: Old values.
        :param new_values: New values.
        :return: Transformed (immutable) or self (mutable).
        """
        pairs = itertools.chain.from_iterable(zip(range(index, stop), new_values))
        new_state = self._state.mset(*pairs)  # type: ignore
        new_self = copy.copy(self)
        new_self._state = new_state
        return new_self

    def _do_insert(self, index, new_values):
        # type: (LD, int, tuple[T, ...]) -> LD
        """
        Insert value(s) at index (internal).

        :param index: Index.
        :param new_values: New values.
        :return: Transformed (immutable) or self (mutable).
        """
        if index == len(self._state):
            new_state = self._state.extend(new_values)
        elif index == 0:
            new_state = pvector(new_values) + self._state
        else:
            new_state = self._state[:index] + pvector(new_values) + self._state[index:]
        new_self = copy.copy(self)
        new_self._state = new_state
        return new_self

    def _do_move(self, target_index, index, stop, post_index, post_stop, values):
        # type: (LD, int, int, int, int, int, tuple[T, ...]) -> LD
        """
        Move values internally (internal).

        :param target_index: Target index.
        :param index: Index (pre-move).
        :param index: Stop (pre-move).
        :param post_index: Post index (post-move).
        :param post_index: Post stop (post-move).
        :param values: Values being moved.
        :return: Transformed (immutable) or self (mutable).
        """
        state = self._state.delete(index, stop)
        if post_index == len(state):
            new_state = state.extend(values)
        elif post_index == 0:
            new_state = pvector(values) + state
        else:
            new_state = state[:post_index] + pvector(values) + state[post_index:]
        new_self = copy.copy(self)
        new_self._state = new_state
        return new_self

    def _do_delete(self, index, stop, old_values):
        # type: (LD, int, int, tuple[T, ...]) -> LD
        """
        Delete values at index/slice (internal).

        :param index: Index.
        :param index: Stop.
        :param old_values: Values being deleted.
        :return: Transformed (immutable) or self (mutable).
        """
        new_state = self._state.delete(index, stop)
        new_self = copy.copy(self)
        new_self._state = new_state
        return new_self


LD = TypeVar("LD", bound=ListData)  # dictionary data self type
