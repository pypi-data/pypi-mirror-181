"""Storage configuration models."""
# TODO fw-storage
# - utilize configs for parsing/loading/validation in factory and storage classes
# - update readme with clarified, explicit creds handling
# TODO xfer
# - drop .env support and rename fs.uid->user / gs.sv_acct->app_creds
# - utilize configs for parsing/validation
import abc
import json
import os
import re
import typing as t
from pathlib import Path

from fw_utils import format_query_string as qs
from fw_utils import format_url, parse_url
from pydantic import BaseModel, Field, SecretStr, root_validator, validator
from typing_extensions import Annotated

LOAD_ENV = True  # load creds from envvars (and read file for gs)
REQUIRE_CREDS = True  # raise on missing creds (s3/gs/az)


class StorageConfig(BaseModel, abc.ABC):
    """Storage config model with URL <-> CFG conversion interface."""

    @classmethod
    @abc.abstractmethod
    def from_url(cls, url: str) -> "StorageConfig":
        """Return storage config parsed from a URL."""

    @property
    @abc.abstractmethod
    def safe_url(self) -> str:
        """Return safe storage URL without credentials."""

    @property
    @abc.abstractmethod
    def full_url(self) -> str:
        """Return full storage URL including credentials and options."""

    def dict(self, secret: t.Literal[None, "str", "val"] = None, **kwargs) -> dict:
        """Return model as dictionary with optional secret serialization."""
        data = super().dict(**kwargs)
        for key, value in data.items():
            if isinstance(value, SecretStr):
                if secret == "str":  # serialize as ***
                    data[key] = str(value)  # pragma: no cover
                if secret == "val":  # serialize as val
                    data[key] = value.get_secret_value()
        return data


class FSConfig(StorageConfig):
    """File-System Storage config."""

    type: t.Literal["fs"] = Field(title="FileSystem storage type")
    path: str = Field(title="File-system directory path", example="/mnt/data")
    user: str | None = Field(
        title="Unix user[:group] to set as the owner when creating files",
        examples=["user", "user:group", "1000:1000"],
    )

    @classmethod
    def from_url(cls, url: str) -> "FSConfig":
        """Return FileSystem storage config parsed from a URL."""
        parsed = parse_url(url)
        params = dict(
            type=parsed.pop("scheme"),
            path=parsed.pop("host", "") + parsed.pop("path", ""),
            user=parsed.pop("user", None),
        )
        assert not parsed, f"unexpected {','.join(parsed)} in url {url!r}"
        return cls(**params)

    @property
    def safe_url(self) -> str:
        """Return safe storage URL without custom options."""
        return format_url(scheme=self.type, path=self.path)

    @property
    def full_url(self) -> str:
        """Return full storage URL with all options."""
        return self.safe_url + qs(user=self.user)

    @validator("path", pre=True)
    @classmethod
    def resolve_path(cls, path: str) -> str:
        """Return absolute path with cwd/home/links resolved."""
        return str(Path(path or "").expanduser().resolve())


class S3Config(StorageConfig):
    """Amazon S3 storage config."""

    type: t.Literal["s3"] = Field(title="S3 storage type")
    bucket: str = Field(
        title="AWS S3 bucket name",
        example="s3-bucket",
        min_length=3,
        max_length=63,
        regex=r"^[a-z0-9-.]+$",
    )
    prefix: str = Field("", title="Common object key prefix", example="prefix")

    access_key_id: str | None = Field(
        title="AWS Access Key ID",
        example="AKIAIOSFODNN7EXAMPLE",
        min_length=16,
        max_length=128,
    )
    secret_access_key: SecretStr | None = Field(
        title="AWS Secret Access Key",
        example="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        min_length=40,
    )

    @classmethod
    def from_url(cls, url: str) -> "S3Config":
        """Return Amazon S3 storage config parsed from a URL."""
        parsed = parse_url(url)
        params = dict(
            type=parsed.pop("scheme"),
            bucket=parsed.pop("host"),
            prefix=parsed.pop("path", "").strip("/"),
            access_key_id=parsed.pop("access_key_id", None),
            secret_access_key=parsed.pop("secret_access_key", None),
        )
        assert not parsed, f"unexpected {','.join(parsed)} in url {url!r}"
        return cls(**params)

    @property
    def safe_url(self) -> str:
        """Return safe storage URL without credentials."""
        return format_url(scheme=self.type, host=self.bucket, path=self.prefix)

    @property
    def full_url(self) -> str:
        """Return full storage URL with credentials."""
        data = self.dict(secret="val")
        return self.safe_url + qs(
            access_key_id=data["access_key_id"],
            secret_access_key=data["secret_access_key"],
        )

    @root_validator(pre=True)
    @classmethod
    def load_creds(cls, values: dict) -> dict:
        """Load creds from the env if enabled."""
        if LOAD_ENV:
            if not values["access_key_id"]:
                values["access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID")
            if not values["secret_access_key"]:
                values["secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY")
        if REQUIRE_CREDS:
            assert values["access_key_id"], "missing required s3 access_key_id"
            assert values["secret_access_key"], "missing required s3 secret_access_key"
        return values


GOOGLE_SERVICE_ACCOUNT_JSON_EXAMPLE = """{
"type": "service_account",
"project_id": "project-id",
"private_key_id": "key-id",
"private_key": "-----BEGIN PRIVATE KEY-----\\nKEY\\n-----END PRIVATE KEY-----\\n",
"client_id": "client-id",
"client_email": "service-account-email",
"auth_uri": "https://accounts.google.com/o/oauth2/auth",
"token_uri": "https://accounts.google.com/o/oauth2/token",
"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-account-email"
}
"""


class GSConfig(StorageConfig):
    """Google Cloud Storage config."""

    type: t.Literal["gs"] = Field(title="Google Cloud Storage type")
    bucket: str = Field(
        title="Google Cloud Storage bucket name",
        example="gs-bucket",
        min_length=3,
        max_length=63,
        regex=r"^[a-z0-9-_.]+$",
    )
    prefix: str = Field("", title="Common object key prefix", example="prefix")

    application_credentials: SecretStr | None = Field(
        title="Google Service Account Key path or contents",
        examples=[
            "~/google_service_account.json",
            GOOGLE_SERVICE_ACCOUNT_JSON_EXAMPLE,
        ],
    )

    @classmethod
    def from_url(cls, url: str) -> "GSConfig":
        """Return Google Cloud Storage config parsed from a URL."""
        parsed = parse_url(url)
        creds = parsed.pop("application_credentials", None)
        # TODO consider not splitting qparams on commas when parsing
        # TODO consider urlsafe_b64en/decode
        creds = ",".join(creds) if isinstance(creds, list) else creds
        params = dict(
            type=parsed.pop("scheme"),
            bucket=parsed.pop("host"),
            prefix=parsed.pop("path", "").strip("/"),
            application_credentials=creds,
        )
        assert not parsed, f"unexpected {','.join(parsed)} in url {url!r}"
        return cls(**params)

    @property
    def safe_url(self) -> str:
        """Return safe storage URL without credentials."""
        return format_url(scheme=self.type, host=self.bucket, path=self.prefix)

    @property
    def full_url(self) -> str:
        """Return full storage URL with credentials."""
        creds = self.dict(secret="val")["application_credentials"]
        return self.safe_url + qs(application_credentials=creds)

    @validator("application_credentials", pre=True)
    @classmethod
    def load_creds(cls, application_credentials: str | None) -> str | None:
        """Return creds read from disk if provided as a file path."""
        creds = application_credentials or ""
        if LOAD_ENV and not creds:
            creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or ""
        if REQUIRE_CREDS:
            assert creds, "missing required gs application_credentials"
        # TODO consider using a try/except flow instead
        if LOAD_ENV and creds and not creds.strip().startswith("{"):  # json test
            creds = Path(creds).expanduser().read_text(encoding="utf8")
        # creds are now the portable json contents - run some checks
        if creds:
            creds_obj = json.loads(creds)
            assert isinstance(creds_obj, dict), "invalid gs credentials (not a dict)"
            assert "type" in creds_obj, "invalid gs credentials (missing type)"
        return creds or None


AZ_BLOB_DOMAIN = "blob.core.windows.net"


class AZConfig(StorageConfig):
    """Azure Blob Storage config."""

    type: t.Literal["az"] = Field(title="Azure Blob Storage type")
    account: str = Field(
        title="Azure Storage Account name",
        example="azaccount",
        min_length=3,
        max_length=23 + (1 + len(AZ_BLOB_DOMAIN)),
        regex=r"^[a-z0-9]+" + re.escape(f".{AZ_BLOB_DOMAIN}") + r"$",
    )
    container: str = Field(
        title="Azure Blob Container name",
        example="container",
        min_length=3,
        max_length=63,
        regex=r"[a-z0-9-]+",
    )
    prefix: str = Field("", title="Common blob key prefix", example="prefix")

    access_key: SecretStr | None = Field(
        title="Azure Storage Account shared Access Key",
        example=(
            "J94I0uS13Cc79AvAq33Hrkt3+C40yq16IF058yQUyiM7"
            "U2qBwGJXQ2VIrLhy0gwGRWMQ2OLTpJ6C9PsEXAMPLE=="
        ),
    )

    tenant_id: str | None = Field(
        title="Azure tenant ID",
        example="c88032d3-19d1-4040-b9bf-b84c29a49480",
    )
    client_id: str | None = Field(
        title="Registered application Client ID",
        example="94ade9ae-5cd7-44ad-8e18-8331e5e3328e",
    )
    client_secret: SecretStr | None = Field(
        title="Registered application Client secret",
        example="o0O8Q~Rou2PCGn.NHGdLLneBQ4xG.fNEXAMPLE~9",
    )

    @classmethod
    def from_url(cls, url: str) -> "AZConfig":
        """Return Azure Blob Storage config parsed from a URL."""
        parsed = parse_url(url)
        path = parsed.pop("path", "").strip("/")
        if "/" in path:
            container, prefix = path.split("/", maxsplit=1)
        else:
            container, prefix = path, ""
        params = dict(
            type=parsed.pop("scheme"),
            account=parsed.pop("host"),
            container=container,
            prefix=prefix,
            access_key=parsed.pop("access_key", None),
            tenant_id=parsed.pop("tenant_id", None),
            client_id=parsed.pop("client_id", None),
            client_secret=parsed.pop("client_secret", None),
        )
        assert not parsed, f"unexpected {','.join(parsed)} in url {url!r}"
        return cls(**params)

    @property
    def safe_url(self) -> str:
        """Return safe storage URL without credentials."""
        path = f"{self.container}/{self.prefix}" if self.prefix else self.container
        return format_url(scheme=self.type, host=self.account, path=path)

    @property
    def full_url(self) -> str:
        """Return full storage URL with credentials."""
        data = self.dict(secret="val")
        return self.safe_url + qs(
            access_key=data["access_key"],
            tenant_id=data["tenant_id"],
            client_id=data["client_id"],
            client_secret=data["client_secret"],
        )

    @validator("account", pre=True)
    @classmethod
    def account_url(cls, account: str) -> str:
        """Return account name with default blob domain unless given a URL."""
        return account if "." in account else f"{account}.{AZ_BLOB_DOMAIN}"

    @root_validator(pre=True)
    @classmethod
    def load_creds(cls, values: dict) -> dict:
        """Load creds from the env if enabled."""
        if LOAD_ENV:
            if not values["access_key"]:
                values["access_key"] = os.getenv("AZURE_ACCESS_KEY")
            if not values["tenant_id"]:
                values["tenant_id"] = os.getenv("AZURE_TENANT_ID")
            if not values["client_id"]:
                values["client_id"] = os.getenv("AZURE_CLIENT_ID")
            if not values["client_secret"]:
                values["client_secret"] = os.getenv("AZURE_CLIENT_SECRET")
        if REQUIRE_CREDS:
            key_groups = [["access_key"], ["tenant_id", "client_id", "client_secret"]]
            msg = "missing required az access_key"  # TODO mention the alternatives
            assert any(all(values[key] for key in keys) for keys in key_groups), msg
        return values


Config = Annotated[
    t.Union[FSConfig, S3Config, GSConfig, AZConfig],
    Field(discriminator="type"),
]
