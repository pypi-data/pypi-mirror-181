import estruttura
from tippo import Any, Callable, Iterable, Type, TypeVar

from .serializers import Serializer, TypedSerializer

__all__ = ["Relationship"]


T = TypeVar("T")


class Relationship(estruttura.Relationship[T]):
    """Describes a relationship between the data and the values it contains."""

    __slots__ = ()

    def __init__(
        self,
        converter=None,  # type: Callable[[Any], T] | Type[T] | str | None
        validator=None,  # type: Callable[[Any], None] | str | None
        types=(),  # type: Iterable[Type[T] | str | None] | Type[T] | str | None
        subtypes=False,  # type: bool
        serializer=TypedSerializer(),  # type: Serializer[T] | None
        extra_paths=(),  # type: Iterable[str]
        builtin_paths=None,  # type: Iterable[str] | None
    ):
        # type: (...) -> None
        """
        :param converter: Callable value converter.
        :param validator: Callable value validator.
        :param types: Types for runtime checking.
        :param subtypes: Whether to accept subtypes.
        :param serializer: Serializer.
        :param extra_paths: Extra module paths in fallback order.
        :param builtin_paths: Builtin module paths in fallback order.
        """
        super(Relationship, self).__init__(
            converter=converter,
            validator=validator,
            types=types,
            subtypes=subtypes,
            serializer=serializer,
            extra_paths=extra_paths,
            builtin_paths=builtin_paths,
        )
