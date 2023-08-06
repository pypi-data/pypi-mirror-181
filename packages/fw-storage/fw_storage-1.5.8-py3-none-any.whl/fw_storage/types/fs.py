"""Local storage module."""
import os
import re
import shutil
import typing as t
from pathlib import Path

import fw_utils

from .. import Storage, errors
from ..fileinfo import FileInfo
from ..filters import STORAGE_FILTERS
from ..storage import AnyPath

__all__ = ["FileSystem"]

# TODO parametrize, basesettings
CHUNKSIZE = 8 << 20


fs_error_map: dict = {
    FileExistsError: errors.FileExists,
    FileNotFoundError: errors.FileNotFound,
    IsADirectoryError: errors.IsADirectory,
    NotADirectoryError: errors.NotADirectory,
    PermissionError: errors.PermError,
    OSError: errors.StorageError,
}


def convert_fs_error(exc: Exception) -> t.Type[errors.StorageError]:
    """Return specific FS errors mapped to StorageError types."""
    return fs_error_map.get(type(exc), errors.StorageError)


errmap = errors.ErrorMapper(*fs_error_map, convert=convert_fs_error)


class FileSystem(Storage):
    """Storage class for locally mounted filesystems."""

    url_re = re.compile(r"fs://(?P<path>[^?]*)(\?(?P<query>[^#]+))?")

    def __init__(
        self,
        path: t.Union[str, Path] = "",
        user: str = None,
    ) -> None:
        """Init FileSystem storage from a path (default: cwd)."""
        path = Path(path) if path else Path.cwd()
        self.prefix = path.expanduser().resolve()
        self.user = user

    def abspath(self, path: AnyPath) -> str:
        """Return absolute path string."""
        return f"{self.prefix}/{self.relpath(path)}"

    def fullpath(self, path: AnyPath) -> str:
        """Return absolute path string including the storage URL."""
        return f"fs://{self.abspath(path)}"

    @errmap
    def ls(  # pylint: disable=arguments-differ
        self,
        path: AnyPath = "",
        *,
        include: fw_utils.Filters = None,
        exclude: fw_utils.Filters = None,
        followlinks: bool = False,
        **_,
    ) -> t.Iterator[FileInfo]:
        """Yield each item under prefix matching the include/exclude filters."""
        # pylint: disable=too-many-locals
        # TODO consider adding in some retries/tolerance for network mounts
        top = Path(f"{self.prefix}/{path}").resolve()
        filt = StorageFilter(include=include, exclude=exclude)
        rel_dirs: t.List[str] = []
        rel_files: t.List[str] = []
        # raise exceptions in os.walk on errors
        def onerr(exc: OSError):  # pragma: no cover
            raise exc

        for root, dirs, files in os.walk(top, followlinks=followlinks, onerror=onerr):

            def rel(name: str) -> str:
                """Return path relative to prefix for given file/dir-name."""
                # pylint: disable=cell-var-from-loop
                return re.sub(rf"^{self.prefix}", "", f"{root}/{name}").strip("/")

            # remove first dir from dirs buffer since it's the current root dir
            if rel_dirs:
                # make sure that this invariant is true
                assert rel_dirs.pop(0) == rel("")
            # sort the dirs to enforce deterministic walk order
            # apply the dir filters to efficiently prune the walk tree
            dirs.sort()
            dirs[:] = [d for d in dirs if filt.match(rel(d), exclude_only=["dir"])]
            # apply the path filters before using os.stat for efficiency
            files = [rel(f) for f in files if filt.match(rel(f), exclude_only=["path"])]
            # keep relative dir and file pathes in a buffer to help
            # interleaving the dirs and files to have total ordering
            rel_dirs.extend([rel(d) for d in dirs])
            rel_dirs.sort()
            rel_files.extend(files)
            rel_files.sort()

            while rel_files:
                if rel_dirs and rel_dirs[0] < rel_files[0]:
                    # stop yield if the next dir is before
                    # the current file in sort order
                    break

                # yield the matching files from this dir
                info = self.stat(rel_files.pop(0))
                if filt.match(info):
                    yield info

    @errmap
    def stat(self, path: AnyPath) -> FileInfo:
        """Return FileInfo using os.stat for a single file."""
        stat = Path(f"{self.prefix}/{path}").stat()
        return FileInfo(
            path=str(path),
            size=stat.st_size,
            hash=None,  # TODO speed consideration
            created=stat.st_ctime,
            modified=stat.st_mtime,
        )

    @errmap
    def get(self, path: AnyPath, **_) -> fw_utils.BinFile:
        """Open file for reading in binary mode."""
        return fw_utils.BinFile(self.abspath(path), metapath=self.relpath(path))

    @errmap
    def set(self, path: AnyPath, file: fw_utils.AnyFile) -> None:
        """Write file to the given storage path."""
        path_ = Path(self.abspath(path))
        path_.parent.mkdir(parents=True, exist_ok=True)
        with fw_utils.open_any(file) as r_file:
            with fw_utils.open_any(path_, mode="wb") as w_file:
                data = r_file.read(CHUNKSIZE)
                while data:
                    w_file.write(data)
                    data = r_file.read(CHUNKSIZE)
        if self.user:
            path_parts = path_.relative_to(self.prefix).parts
            user = [int(id_) for id_ in self.user.split(":")]
            for i in range(len(path_parts)):
                rel_p = "/".join(path_parts[: i + 1])
                shutil.chown(self.prefix / rel_p, *user)  # type: ignore

    @errmap
    def rm(self, path: AnyPath, recurse: bool = False) -> None:
        """Remove a file at the given path."""
        path_ = Path(self.abspath(path))
        if path_.is_dir():
            if not recurse:
                raise ValueError("Cannot remove dir (use recurse=True)")
            shutil.rmtree(path_)
        else:
            path_.unlink()

    @errmap
    def rm_empty_dirs(self):
        """Remove empty directories."""
        deleted_dirs = set()
        for root, dirs, files in os.walk(self.prefix, topdown=False):
            if root == str(self.prefix):
                return
            if not files and all(f"{root}/{dir}" in deleted_dirs for dir in dirs):
                os.rmdir(root)
                deleted_dirs.add(root)


# FILTERING


class DirFilter(fw_utils.StringFilter):
    """File system storage directory filter."""

    def match(self, value) -> bool:
        """Match str with the filter's regex pattern."""
        if not isinstance(value, str):
            value = getattr(value, self.field, getattr(value, "path"))
        return super().match(value)


FS_STORAGE_FILTERS: t.Dict[str, t.Type[fw_utils.ExpressionFilter]] = {
    "dir": DirFilter,
    **STORAGE_FILTERS,
}


def validate_storage_field(field: str) -> str:
    """Return validated/canonic storage field name for the field shorthand."""
    return fw_utils.parse_field_name(field, allowed=list(FS_STORAGE_FILTERS))


class StorageFilter(fw_utils.IncludeExcludeFilter):
    """Storage include/exclude filter with field validation and filter types."""

    def __init__(
        self,
        include: fw_utils.Filters = None,
        exclude: fw_utils.Filters = None,
    ) -> None:
        """Init filter with field name validators and filter types."""
        super().__init__(
            FS_STORAGE_FILTERS,
            include=include,
            exclude=exclude,
            validate=validate_storage_field,
        )
