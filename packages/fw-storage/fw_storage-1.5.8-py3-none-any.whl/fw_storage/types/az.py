"""Azure blob storage module."""
import functools
import io
import os
import re
import stat
import typing as t

import azure.core.exceptions as az_errors
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient, _blob_client
from azure.storage.blob._shared.policies import StorageRetryPolicy
from fw_utils import AnyFile, Filters, open_any
from pydantic import BaseSettings

from .. import errors
from ..fileinfo import FileInfo
from ..filters import StorageFilter
from ..storage import AnyPath, CloudStorage

__all__ = ["AzureBlob"]


def create_default_client(
    account: str,
    container: str,
    access_key: str = None,
    **kwargs,
) -> ContainerClient:
    """Azure Blob Container Client factory.

    Uses the Azure Access Key passed in directly OR provided via the envvar
    AZURE_ACCESS_KEY.

    See the Azure docs for the full list of supported credential sources:
    https://docs.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential
    """
    access_key = str(access_key or os.getenv("AZURE_ACCESS_KEY") or "")
    from_creds = functools.partial(ContainerClient, account, container)
    retry_policy = AzureRetryPolicy(RetryConfig())
    if access_key:  # pragma: no cover
        # TODO remove cover
        return from_creds(credential=str(access_key), retry_policy=retry_policy)
    if SAS_QUERY_PARAMS.intersection(set(kwargs)):
        sas_params = [
            f"{param}={kwargs.pop(param)}"
            for param in SAS_QUERY_PARAMS
            if param in kwargs
        ]
        sas_url = f"https://{account}/{container}?{'&'.join(sas_params)}"
        return ContainerClient.from_container_url(sas_url, retry_policy=retry_policy)
    return from_creds(credential=DefaultAzureCredential(), retry_policy=retry_policy)


class RetryConfig(BaseSettings):
    """Retry config."""

    class Config:
        env_prefix = "AZURE_RETRY_"

    total: int = 3
    backoff_factor: float = 0.5


class AzureRetryPolicy(StorageRetryPolicy):
    """Custom Azure retry policy."""

    def __init__(self, config: RetryConfig):
        self.backoff_factor = config.backoff_factor
        super().__init__(retry_total=config.total, retry_to_secondary=False)

    def get_backoff_time(self, settings):  # pragma: no cover
        """Calculates how long to sleep before retrying."""
        # TODO re-add cover
        return self.backoff_factor * (2 ** settings["count"] - 1)


az_error_map = {
    az_errors.ClientAuthenticationError: errors.PermError,
    az_errors.ResourceNotFoundError: errors.FileNotFound,
    az_errors.ResourceExistsError: errors.FileExists,
    az_errors.AzureError: errors.StorageError,
}


def convert_az_error(exc: Exception) -> t.Type[errors.StorageError]:
    """Return specific AZ errors mapped to StorageError types."""
    return az_error_map.get(type(exc), errors.StorageError)


errmap = errors.ErrorMapper(*az_error_map, convert=convert_az_error)


class AzureBlob(CloudStorage):
    """Azure Blob Storage class."""

    # NOTE Azure only supports up to 256 subrequests in a single batch
    delete_batch_size: t.ClassVar[int] = 256

    url_re = re.compile(
        r"az://(?P<account>[^/]+)/(?P<container>[^:/?#]+)"
        r"(/(?P<prefix>[^?#]+))?"
        r"(\?(?P<query>[^#]+))?"
    )

    def __init__(
        # pylint: disable=too-many-arguments
        self,
        account: str,
        container: str,
        prefix: str = "",
        access_key: str = None,
        create_client: t.Callable = None,
        **kwargs,
    ) -> None:
        """Construct Azure storage."""
        self.account = account
        self.container = container
        self.prefix = prefix
        create_client = create_client or create_default_client
        self.client = create_client(account, container, access_key, **kwargs)
        # TODO fix behavior on missing credentials
        # currently az only tries to get a token on ls/get/set, which
        # in turn is retried and thus results in very ugly logs and delays
        # Below is a failed attempt to get a token w/o retries - needs scopes
        # self.client.credential.get_token()  # force checking *some* creds
        super().__init__(**kwargs)

    def abspath(self, path: AnyPath) -> str:
        """Return path string relative to the storage URL, including the perfix."""
        return f"{self.prefix}/{self.relpath(path)}".lstrip("/")

    def fullpath(self, path: AnyPath) -> str:
        """Return path string including the storage URL and prefix."""
        return f"az://{self.account}/{self.container}/{self.abspath(path)}".rstrip("/")

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
        path = self.abspath(path)
        filt = StorageFilter(include=include, exclude=exclude)
        for blob in self.client.list_blobs(name_starts_with=path):
            relpath = re.sub(rf"^{self.prefix}", "", blob.name).lstrip("/")
            info = FileInfo(
                path=relpath,
                size=blob.size,
                hash=blob.etag,  # pylint: disable=duplicate-code
                created=blob.creation_time.timestamp(),
                modified=blob.last_modified.timestamp(),
            )
            # skip az "folders" - path is empty if the prefix itself is a "folder"
            if not relpath or relpath.endswith("/") and info.size == 0:
                continue  # pragma: no cover
            if filt.match(info):
                yield info

    @errmap
    def stat(self, path: AnyPath) -> FileInfo:
        """Return FileInfo for a single file."""
        blob_client = self.client.get_blob_client(self.abspath(path))
        blob = blob_client.get_blob_properties()
        return FileInfo(
            path=str(path),
            size=blob.size,
            hash=blob.etag,
            created=blob.creation_time.timestamp(),
            modified=blob.last_modified.timestamp(),
        )

    @errmap
    def download_file(self, path: str, dst: t.IO[bytes]) -> None:
        """Download file and it is opened for reading in binary mode."""
        blob_stream = self.client.download_blob(path)
        blob_stream.readinto(dst)

    @errmap
    def upload_file(self, path: str, file: AnyFile) -> None:
        """Write source file to the given path."""
        # upload_blob uses automatic chunking stated by Azure documentation
        with open_any(file, mode="rb") as r_file:
            self.client.upload_blob(name=path, data=r_file, overwrite=True)

    @errmap
    def flush_delete(self) -> None:
        """Remove a file at the given path."""
        self.client.delete_blobs(*self.delete_keys, delete_snapshots="include")
        self.delete_keys.clear()


# patch Azure SDK's get_length to support streaming from requests (sockets)
# see: https://flywheelio.atlassian.net/browse/FLYW-11776

orig_get_length = _blob_client.get_length


def get_length_patch(data) -> t.Optional[int]:
    """Return None instead of 0 if data is a socket."""
    try:
        fileno = data.fileno()
        fstat = os.fstat(fileno)
        if stat.S_ISSOCK(fstat.st_mode):
            return None
    except (AttributeError, OSError, io.UnsupportedOperation):
        pass
    return orig_get_length(data)


_blob_client.get_length = get_length_patch


SAS_QUERY_PARAMS: set = {
    "sp",
    "st",
    "se",
    "skoid",
    "sktid",
    "skt",
    "ske",
    "sks",
    "skv",
    "saoid",
    "suoid",
    "scid",
    "sip",
    "spr",
    "sv",
    "sr",
    "rscc",
    "rscd",
    "rsce",
    "rscl",
    "rsct",
    "sig",
}
