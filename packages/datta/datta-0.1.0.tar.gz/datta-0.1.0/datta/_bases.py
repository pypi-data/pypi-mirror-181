import six
from estruttura import (
    BaseImmutableCollectionStructure,
    BaseImmutableStructure,
    BaseStructureMeta,
    BaseUserImmutableCollectionStructure,
    BaseUserImmutableStructure,
)
from tippo import TypeVar

T_co = TypeVar("T_co", covariant=True)


class BaseDataMeta(BaseStructureMeta):
    """Metaclass for :class:`BasePrivateData`."""


# noinspection PyAbstractClass
class BasePrivateData(six.with_metaclass(BaseDataMeta, BaseImmutableStructure)):
    """Base private data."""

    __slots__ = ()


# noinspection PyAbstractClass
class BaseData(BasePrivateData, BaseUserImmutableStructure):
    """Base data."""

    __slots__ = ()


# noinspection PyAbstractClass
class PrivateDataCollection(BasePrivateData, BaseImmutableCollectionStructure[T_co]):
    """Private data collection."""

    __slots__ = ()


# noinspection PyAbstractClass
class DataCollection(PrivateDataCollection[T_co], BaseUserImmutableCollectionStructure[T_co]):
    """Base data collection."""

    __slots__ = ()

    def _do_clear(self):
        return type(self)()
