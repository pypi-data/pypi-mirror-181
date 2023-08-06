"""Storage errors."""
import functools
import inspect
import typing as t

from fw_utils.formatters import quantify

__all__ = [
    "FileExists",
    "FileNotFound",
    "IsADirectory",
    "NotADirectory",
    "PermError",
    "StorageError",
]


class StorageError(Exception):
    """Base exception class for all storage errors."""

    def __init__(
        self,
        message: str = "",  # for direct usage (custom messages)
        errors: list = None,  # for direct usage (sub-errors, eg. batch op)
        context: str = None,  # auto-filled via add_context / ErrorMapper
        raw_exc: Exception = None,  # auto-filled via add_context / ErrorMapper
    ):
        """Init StorageError instance."""
        super().__init__(message)
        self.message = message
        self.errors = errors
        self.context = context
        self.raw_exc = raw_exc

    def add_context(self, exc, func, args, kwargs):
        """Add storage method, path and 3rd-party error context."""
        storage = args[0]
        relpath = args[1] if len(args) > 1 else kwargs.get("path", "")
        self.context = f"{func.__name__}({storage.fullpath(relpath)!r})"
        self.raw_exc = exc

    def __str__(self) -> str:  # pragma: no cover
        """Return stringified error."""
        raw_exc_str = format_exc(self.raw_exc) if self.raw_exc else None
        parts = [s for s in [self.message, self.context, raw_exc_str] if s]
        exc_str = ": ".join(parts)
        if self.errors:
            exc_str = "\n - ".join([exc_str] + self.errors[:5])
            err_cnt = len(self.errors)
            if err_cnt > 5:
                exc_str += f"\n - and {quantify(err_cnt -5, 'more error')}"
        return exc_str


class PermError(StorageError):
    """Permission error. Raised when roles/permissions are insufficient."""


class FileNotFound(StorageError):
    """File not found. Raised when trying to access a file that doesn't exist."""


class FileExists(StorageError):
    """File already exists. Raised when trying to create a file that's present."""


class IsADirectory(StorageError):
    """Path is a directory. Raised when a file operation is used on a dir."""


class NotADirectory(StorageError):
    """Path is not a directory. Raised when a dir operation is used on a file."""


def format_exc(exc: Exception) -> str:  # pragma: no cover
    """Return exception type and message formatted as in tracebacks."""
    # NOTE only works with instances - add cls support later if needed
    return f"{exc.__class__.__module__}.{exc.__class__.__name__}: {exc}"


class ErrorMapper:
    """Parameterized decorator for raising StorageErrors from 3rd-party exceptions."""

    def __init__(
        self,
        *errors: t.Type[Exception],
        convert: t.Callable[[Exception], t.Union[t.Type[StorageError], StorageError]],
    ):
        """Init the decorator with the errors to catch and the conversion func."""
        super().__init__()
        self.errors = errors
        self.convert = convert

    def map(self, exc, func, args, kwargs) -> StorageError:
        """Return StorageError with context converted from a raw exception."""
        mapped = self.convert(exc)
        mapped = mapped() if inspect.isclass(mapped) else mapped
        assert isinstance(mapped, StorageError)
        mapped.add_context(exc, func, args, kwargs)
        return mapped

    def __call__(self, func: t.Callable) -> t.Callable:
        """Decorate the given function to raise StorageErrors."""
        # pylint: disable=catching-non-exception
        # TODO consider popping stack frame(s) to hide this decorator
        # TODO consider re-using the orig stack and raising from None
        if inspect.isgeneratorfunction(func):

            def wrapper(*args, **kwargs):
                try:
                    yield from func(*args, **kwargs)
                except self.errors as exc:
                    raise self.map(exc, func, args, kwargs) from exc

        else:

            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except self.errors as exc:
                    raise self.map(exc, func, args, kwargs) from exc

        return functools.wraps(func)(wrapper)
