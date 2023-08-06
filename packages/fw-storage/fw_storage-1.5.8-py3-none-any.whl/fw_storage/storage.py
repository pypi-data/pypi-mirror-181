"""Storage base class and factory."""
import abc
import importlib
import shutil
import typing as t
from pathlib import Path
from tempfile import gettempdir, mkdtemp

from diskcache import Cache
from fw_utils import AnyFile, BinFile, TempFile, parse_url
from memoization import cached

from .fileinfo import FileInfo

DEFAULT_CACHE_SIZE = 1 << 30  # 1GB
SPOOLED_TMP_MAX_SIZE = 1 << 20  # 1MB
# map of url schemes to storage class import paths (and user-registered classes)
# TODO fw:// storage class
STORAGE_CLASSES: t.Dict[str, t.Union[str, t.Type["Storage"]]] = {
    "fs": "fw_storage.types.fs.FileSystem",
    "s3": "fw_storage.types.s3.S3",
    "gs": "fw_storage.types.gs.GoogleCloudStorage",
    "az": "fw_storage.types.az.AzureBlob",
    "dicom": "fw_storage.types.dicom.DICOM",
    "dicomweb": "fw_storage.types.dicomweb.DICOMweb",
}

AnyPath = t.Union[str, FileInfo]


class Storage(abc.ABC):
    """Abstract storage class defining the common interface."""

    # URL regex to parse and capture init args with
    url_re: t.ClassVar[t.Pattern]

    @staticmethod
    def relpath(path: AnyPath) -> str:
        """Return path string relative to the storage prefix."""
        return str(path).lstrip("/")

    @abc.abstractmethod
    def abspath(self, path: AnyPath) -> str:
        """Return path string relative to the storage URL, including the perfix."""

    @abc.abstractmethod
    def fullpath(self, path: AnyPath) -> str:
        """Return path string including the storage URL and prefix."""

    @abc.abstractmethod
    def ls(
        self,
        path: AnyPath = "",
        *,
        include: t.Optional[t.List[str]] = None,
        exclude: t.Optional[t.List[str]] = None,
        **kwargs,
    ) -> t.Iterator[FileInfo]:
        """Yield items under path that match the include/exclude filters."""

    @abc.abstractmethod
    def stat(self, path: AnyPath) -> FileInfo:
        """Return FileInfo for a given path."""

    @abc.abstractmethod
    def get(self, path: AnyPath, **kwargs) -> BinFile:
        """Return a file opened in binary reading mode."""

    @abc.abstractmethod
    def set(self, path: AnyPath, file: AnyFile) -> None:
        """Write a file at a given path in storage."""

    @abc.abstractmethod
    def rm(self, path: AnyPath, recurse: bool = False) -> None:
        """Remove a file from storage."""

    # TODO add opt-in perf testing
    def test_read(self):
        """Verify read access (list files then stat/get the 1st)."""
        file = stat = None
        for file in self.ls():
            stat = self.stat(file)
            break
        # TODO implement get(path, stream=True) instead...
        if file and stat and stat.size < 1 << 20:  # < 1MB
            self.get(file)
        self.cleanup()

    def test_write(self):
        """Verify write access (create/remove a test file)."""
        self.set("flywheel-write-test", b"flywheel-write-test")
        self.rm("flywheel-write-test")
        self.cleanup()

    def cleanup(self) -> None:
        """Run any cleanup steps for the storage (eg. tempfiles, buffers)."""

    def __enter__(self):
        """Enter storage 'with' context to enable automatic cleanup()."""
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        """Invoke cleanup() when exiting the storage 'with' context."""
        self.cleanup()

    def __del__(self) -> None:
        """Invoke cleanup() when the storage is garbage-collected."""
        self.cleanup()

    def __str__(self) -> str:  # pragma: no cover
        """Return string representation of the storage."""
        return f"{self.__class__.__name__}({self.fullpath('')!r})"


class CloudStorage(Storage):
    """Base class for Cloud Storages."""

    delete_batch_size: t.ClassVar[int] = 1000

    def __init__(
        self,
        *_args,
        cache_dir: str = None,
        cache_size: int = DEFAULT_CACHE_SIZE,
        **_kwargs,
    ):
        """Initialize cloud storage, check permission and setup cache."""
        self._cache = None
        self.cache_root = cache_dir or gettempdir()
        self.cache_dir = Path(mkdtemp(prefix="fw-storage-", dir=self.cache_root))
        self.cache_size = int(cache_size)
        self.delete_keys: t.Set[str] = set()

    @abc.abstractmethod
    def download_file(self, path: str, dst: t.IO[bytes]) -> None:
        """Download file and it opened for reading in binary mode."""

    @abc.abstractmethod
    def upload_file(self, path: str, file: AnyFile) -> None:
        """Upload file to the given path."""

    @abc.abstractmethod
    def flush_delete(self):
        """Flush pending remove operations."""

    @property
    def cache(self):
        """Get underlying cache object.

        Cache is created on the first access or recreated
        if cleanup was called in the meantime.
        """
        if not self._cache and self.cache_size > 0:
            self._cache = Cache(
                directory=self.cache_dir,
                size_limit=self.cache_size,
                eviction_policy="least-recently-used",
            )
        return self._cache

    def cache_get(self, key: str) -> t.Optional[t.BinaryIO]:
        """Get item from cache if enabled."""
        if self.cache is not None:
            return t.cast(t.BinaryIO, self.cache.get(key, read=True))
        return None

    def cache_set(self, key: str, file: t.IO[bytes]) -> None:
        """Set cache item if enabled."""
        if self.cache is not None:
            self.cache.set(key, file, read=True)

    def cache_del(self, key: str) -> None:
        """Remove item from cache if enabled."""
        if self.cache is not None:
            self.cache.delete(key)

    def get(  # pylint: disable=arguments-differ
        self, path: AnyPath, cache: bool = True, **_kwargs
    ) -> BinFile:
        """Return a file opened for reading in binary mode."""
        abspath = self.abspath(path)
        if cache:
            cached_file = self.cache_get(abspath)
            if cached_file:
                return BinFile(cached_file, metapath=self.relpath(path))
        file = TempFile()
        self.download_file(abspath, file)
        size = file.tell()
        file.seek(0)
        if cache and size < self.cache_size:
            self.cache_set(abspath, file)
            file.seek(0)
        return BinFile(t.cast(t.BinaryIO, file), metapath=self.relpath(path))

    def set(self, path: AnyPath, file: AnyFile) -> None:
        """Write a file at the given path in storage."""
        path = self.abspath(path)
        file = str(file) if isinstance(file, Path) else file
        self.upload_file(path, file)
        self.cache_del(path)

    def rm(self, path: AnyPath, recurse: bool = False, flush: bool = False) -> None:
        """Remove file from storage.

        Removing objects is delayed and performed in batches (see 'flush_delete').
        """
        if not recurse:
            self.delete_keys.add(self.abspath(path))
        else:
            for file in self.ls(path):
                self.delete_keys.add(self.abspath(file))
                if len(self.delete_keys) >= self.delete_batch_size:
                    self.flush_delete()
        if flush or len(self.delete_keys) >= self.delete_batch_size:
            self.flush_delete()

    def cleanup(self):
        """Flush pending remove operations and clear cache."""
        self._cache = None
        if hasattr(self, "cache_dir"):
            shutil.rmtree(self.cache_dir, ignore_errors=True)
        if hasattr(self, "delete_keys") and self.delete_keys:
            for key in self.delete_keys:
                self.cache_del(key)
            self.flush_delete()


def get_storage(storage_url: str, **kwargs) -> Storage:
    """Return storage instance for a storage URL (factory)."""
    parsed = parse_url(storage_url)
    scheme = parsed["scheme"]
    if scheme not in STORAGE_CLASSES:
        raise ValueError(f"Unknown storage URL scheme {scheme}")
    storage_cls = STORAGE_CLASSES[scheme]
    if isinstance(storage_cls, str):
        storage_cls = get_storage_cls(storage_cls)
    storage_kw = parse_url(storage_url, storage_cls.url_re)
    storage_kw.update(kwargs)
    storage_kw.pop("write", None)  # compat
    # compat fs - uid/gid replaced with user
    if uid := storage_kw.pop("uid", None):
        if gid := storage_kw.pop("gid", None):
            storage_kw.setdefault("user", f"{uid}:{gid}")
        else:
            storage_kw.setdefault("user", f"{uid}")
    # compat gs - service_account_key replaced with application_credentials
    if service_account_key := storage_kw.pop("service_account_key", None):
        storage_kw.setdefault("application_credentials", service_account_key)
    # compat gs - undo qparam comma splitting while fw-utils is pinned
    if app_creds := storage_kw.get("application_credentials", None):
        # TODO get rid of this madness w/ factory rewrite
        if isinstance(app_creds, list):
            storage_kw["application_credentials"] = ",".join(app_creds)
    return storage_cls(**storage_kw)  # type: ignore


@cached
def get_storage_cls(storage_cls_path: str) -> t.Type[Storage]:
    """Return the storage class for an import path (late import)."""
    module_path, cls_name = storage_cls_path.rsplit(".", maxsplit=1)
    try:
        module = importlib.import_module(module_path, cls_name)
        storage_cls = getattr(module, cls_name)
    except (ImportError, AttributeError) as exc:
        msg = f"Cannot import storage class {storage_cls_path} ({exc})"
        raise ValueError(msg) from exc
    return storage_cls
