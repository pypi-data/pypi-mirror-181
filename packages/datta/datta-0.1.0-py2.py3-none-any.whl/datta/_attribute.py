import estruttura
from basicco.namespace import Namespace
from tippo import Any, Callable, Iterable, Mapping, TypeVar

from ._constants import MISSING, MissingType
from ._relationship import Relationship

__all__ = ["Attribute"]


T_co = TypeVar("T_co", covariant=True)


class Attribute(estruttura.Attribute[T_co]):
    __slots__ = ()

    def __init__(
        self,  # type: A
        default=MISSING,  # type: T_co | MissingType
        factory=MISSING,  # type: Callable[..., T_co] | str | MissingType
        relationship=Relationship(),  # type: Relationship[T_co]
        required=None,  # type: bool | None
        init=None,  # type: bool | None
        init_as=None,  # type: A | str | None
        settable=None,  # type: bool | None
        deletable=None,  # type: bool | None
        serializable=None,  # type: bool | None
        serialize_as=None,  # type: A | str | None
        serialize_default=True,  # type: bool
        constant=False,  # type: bool
        repr=None,  # type: bool | Callable[[T_co], str] | None
        eq=None,  # type: bool | None
        order=None,  # type: bool | None
        hash=None,  # type: bool | None
        doc="",  # type: str
        metadata=None,  # type: Any
        namespace=None,  # type: Namespace | Mapping[str, Any] | None
        callback=None,  # type: Callable[[A], None] | None
        extra_paths=(),  # type: Iterable[str]
        builtin_paths=None,  # type: Iterable[str] | None
    ):
        # type: (...) -> None
        """
        :param default: Default value.
        :param factory: Default factory.
        :param relationship: Relationship.
        :param required: Whether it is required to have a value.
        :param init: Whether to include in the `__init__` method.
        :param init_as: Alternative attribute or name to use when initializing.
        :param settable: Whether the value can be changed after being set.
        :param deletable: Whether the value can be deleted.
        :param serializable: Whether it's serializable.
        :param serialize_as: Alternative attribute or name to use when serializing.
        :param serialize_default: Whether to serialize default value.
        :param constant: Whether attribute is a class constant.
        :param repr: Whether to include in the `__repr__` method (or a custom repr function).
        :param eq: Whether to include in the `__eq__` method.
        :param order: Whether to include in the `__lt__`, `__le__`, `__gt__`, `__ge__` methods.
        :param hash: Whether to include in the `__hash__` method.
        :param doc: Documentation.
        :param metadata: User metadata.
        :param namespace: Namespace.
        :param callback: Callback that runs after attribute has been named/owned by class.
        :param extra_paths: Extra module paths in fallback order.
        :param builtin_paths: Builtin module paths in fallback order.
        """
        super(Attribute, self).__init__(
            default=default,
            factory=factory,
            relationship=relationship,
            required=required,
            init=init,
            init_as=init_as,
            settable=settable,
            deletable=deletable,
            serializable=serializable,
            serialize_as=serialize_as,
            serialize_default=serialize_default,
            constant=constant,
            repr=repr,
            eq=eq,
            order=order,
            hash=hash,
            doc=doc,
            metadata=metadata,
            namespace=namespace,
            callback=callback,
            extra_paths=extra_paths,
            builtin_paths=builtin_paths,
        )


A = TypeVar("A", bound=Attribute)
