"""Google Cloud Storage module."""
import re
import typing as t
from pathlib import Path

import google.api_core.exceptions as gs_errors
from fw_utils import AnyFile, Filters, TempDir, TempEnv
from google.cloud.storage import Client
from google.cloud.storage.retry import DEFAULT_RETRY

from .. import errors
from ..fileinfo import FileInfo
from ..filters import StorageFilter
from ..storage import AnyPath, CloudStorage

__all__ = ["GoogleCloudStorage"]

DEFAULT_CONTENT_TYPE = "application/octet-stream"


def create_default_client(application_credentials: str = None) -> Client:
    """Google Cloud Storage Client factory.

    Uses the Google Service Account Key JSON path (or contents) passed in
    directly OR provided via the envvar GOOGLE_APPLICATION_CREDENTIALS.

    See Google's docs for the full list of supported credential sources:
    https://google-auth.readthedocs.io/en/latest/reference/google.auth.html
    """
    creds = "GOOGLE_APPLICATION_CREDENTIALS"
    with TempEnv() as env:
        key = str(application_credentials or env.get(creds) or "")
        if key and key.strip().startswith("{"):
            # extension to allow passing the key *contents* via envvar
            with TempDir() as tmp:
                tmp_key = tmp / "key.json"
                tmp_key.write_text(key)
                env[creds] = str(tmp_key)
                return Client()
        elif key:
            # extension to allow ~tilde expansion in the creds path
            env[creds] = str(Path(key).expanduser())
        # let google sdk gather default credentials from various sources
        return Client()


gs_error_map = {
    gs_errors.NotFound: errors.FileNotFound,
    gs_errors.Forbidden: errors.PermError,
    gs_errors.GoogleAPIError: errors.StorageError,
}


def convert_gs_error(exc: Exception) -> t.Type[errors.StorageError]:
    """Return specific GS errors mapped to StorageError types."""
    return gs_error_map.get(type(exc), errors.StorageError)


errmap = errors.ErrorMapper(*gs_error_map, convert=convert_gs_error)


class GoogleCloudStorage(CloudStorage):
    """Google Cloud Storage class."""

    url_re = re.compile(
        r"gs://(?P<bucket>[^:/?#]+)((?P<prefix>/[^?#]+))?(\?(?P<query>[^#]+))?"
    )

    def __init__(
        self,
        bucket: str,
        *,
        prefix: str = "",
        application_credentials: str = None,
        create_client: t.Callable = None,
        **kwargs,
    ):
        """Google Cloud Storage class for working with blobs in GCS buckets.

        Args:
            bucket: Google Cloud Storage bucket name.
            prefix: Common object key prefix. (optional, default is "")
            application_credentials: Google Service Account Key path or contents.
                (optional, default from SDK)
            create_client: google.cloud.storage.Client factory. (optional)
                (optional, default is create_default_client)
        """
        self.bucket = bucket
        self.prefix = prefix.strip("/")
        create_client = create_client or create_default_client
        self.client = create_client(application_credentials)
        super().__init__(**kwargs)

    def abspath(self, path: AnyPath) -> str:
        """Return path string relative to the storage URL, including the perfix."""
        return f"{self.prefix}/{self.relpath(path)}".lstrip("/")

    def fullpath(self, path: AnyPath) -> str:
        """Return path string including the storage URL and prefix."""
        return f"gs://{self.bucket}/{self.abspath(path)}".rstrip("/")

    @errmap
    def ls(
        self,
        path: AnyPath = "",
        *,
        include: Filters = None,
        exclude: Filters = None,
        **_,
    ) -> t.Iterator[FileInfo]:
        """Yield each item under prefix matching the include/exclude filters."""
        # https://cloud.google.com/storage/docs/folders#gsutil
        # https://cloud.google.com/storage/docs/hashes-etags
        filt = StorageFilter(include=include, exclude=exclude)
        prefix = f"{self.prefix}/{path}".strip("/")
        if prefix:
            prefix += "/"
        for blob in self.client.list_blobs(self.bucket, prefix=prefix):
            relpath = re.sub(rf"^{self.prefix}", "", blob.name).lstrip("/")
            info = FileInfo(
                path=relpath,
                size=blob.size,
                hash=blob.etag,
                created=blob.time_created.timestamp(),
                modified=blob.updated.timestamp(),
            )
            # skip gs "folders" - path is empty if the prefix itself is a "folder"
            if not relpath or relpath.endswith("/") and info.size == 0:
                continue  # pragma: no cover
            if filt.match(info):
                yield info

    @errmap
    def stat(self, path: AnyPath) -> FileInfo:
        """Return FileInfo for a single file."""
        blob = self.client.bucket(self.bucket).blob(self.abspath(path))
        blob.reload()
        return FileInfo(
            path=str(path),
            size=blob.size,
            hash=blob.etag,
            created=blob.time_created.timestamp(),
            modified=blob.updated.timestamp(),
        )

    @errmap
    def download_file(self, path: str, dst: t.IO[bytes]) -> None:
        """Download file and it opened for reading in binary mode."""
        self.client.bucket(self.bucket).blob(path).download_to_file(dst)

    @errmap
    def upload_file(self, path: str, file: AnyFile) -> None:
        """Upload file to the given path."""
        blob = self.client.bucket(self.bucket).blob(path)
        if isinstance(file, bytes):
            upload_func = blob.upload_from_string
        elif isinstance(file, str):
            upload_func = blob.upload_from_filename
        else:
            upload_func = blob.upload_from_file
        # by default, only uploads with if_generation_match set
        # will be retried, override this and retry always for now
        # TODO consider fetching the current generation and use that
        # but it would require one additional request per upload
        # see: https://cloud.google.com/storage/docs/generations-preconditions
        upload_func(file, content_type=DEFAULT_CONTENT_TYPE, retry=DEFAULT_RETRY)

    @errmap
    def flush_delete(self):
        """Flush pending remove operations."""
        for key in sorted(self.delete_keys):
            self.client.bucket(self.bucket).blob(key).delete()
            self.delete_keys.remove(key)
