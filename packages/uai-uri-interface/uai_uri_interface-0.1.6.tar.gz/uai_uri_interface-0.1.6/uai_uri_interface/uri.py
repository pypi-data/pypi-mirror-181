from __future__ import annotations

from typing import (
    Any,
    Generator,
    IO,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    runtime_checkable,
    Protocol,
    Literal,
)


BinaryMode = Literal["rb", "wb"]
TextMode = Literal["r", "w"]
SelfType = TypeVar("SelfType", bound="URI")

SupportedMode = Union[BinaryMode, TextMode]


# noinspection PyPropertyDefinition
@runtime_checkable
class URI(Protocol):  # pragma: no cover

    """
    interface for pathlib.Path-like functionality.
    Note that while this interface is very close to pathlib.Path, it is not exactly the same. FlexiPath and all backends
    implement this interface.
    """

    def __init__(self, *pathsegments: Union[str, "URI"]):
        ...

    def __str__(self) -> str:
        ...

    def __truediv__(self: SelfType, key: str) -> SelfType:
        ...

    def __eq__(self, other: Any) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def exists(self) -> bool:
        ...

    def open(
        self,
        mode: SupportedMode,
        buffering: int = -1,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        newline: Optional[str] = None,
    ) -> IO[Any]:
        # https://docs.python.org/3/library/functions.html#open
        ...

    def is_dir(self) -> bool:
        ...

    def is_file(self) -> bool:
        ...

    def mkdir(self, mode: int = 0o777, parents: bool = False, exist_ok: bool = False) -> None:
        ...

    def iterdir(self: SelfType) -> Generator[SelfType, None, None]:
        ...

    def rmdir(self) -> None:
        ...

    def unlink(self) -> None:
        ...

    def with_suffix(self: SelfType, suffix: str) -> SelfType:
        ...

    @property
    def parents(self: SelfType) -> Sequence[SelfType]:
        ...

    @property
    def parent(self: SelfType) -> SelfType:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def stem(self) -> str:
        ...

    @property
    def suffix(self) -> str:
        ...

    @property
    def parts(self) -> Tuple[str, ...]:
        ...
