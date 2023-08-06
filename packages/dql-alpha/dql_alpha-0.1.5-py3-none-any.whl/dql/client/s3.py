from typing import cast

from s3fs import S3FileSystem

from .fsspec import FSSpecClient


class ClientS3(FSSpecClient):
    FS_CLASS = S3FileSystem
    PREFIX = "s3://"
    protocol = "s3"

    def __init__(self, name, **kwargs):
        super().__init__(name, self.create_fs(**kwargs))

    @classmethod
    def create_fs(cls, **kwargs) -> S3FileSystem:
        if "aws_anon" in kwargs:
            kwargs.setdefault("anon", kwargs.pop("aws_anon"))
        if "aws_endpoint_url" in kwargs:
            kwargs.setdefault("client_kwargs", {}).setdefault(
                "endpoint_url", kwargs.pop("aws_endpoint_url")
            )
        if "aws_key" in kwargs:
            kwargs.setdefault("key", kwargs.pop("aws_key"))
        if "aws_secret" in kwargs:
            kwargs.setdefault("secret", kwargs.pop("aws_secret"))
        if "aws_token" in kwargs:
            kwargs.setdefault("token", kwargs.pop("aws_token"))

        return cast(S3FileSystem, super().create_fs(**kwargs))

    @property
    def uri(self):
        return f"s3://{self.name}"

    @staticmethod
    def clean_s3_version(ver):
        return ver if ver != "null" else ""

    @classmethod
    def _df_from_info(cls, v, dir_id, delimiter, path):
        return {
            "dir_id": None,
            "parent_id": dir_id,
            "path": path,
            "name": v.get("Key", "").split(delimiter)[-1],
            # 'expires': expires,
            "checksum": "",
            "etag": v.get("ETag", "").strip('"'),
            "version": ClientS3.clean_s3_version(v.get("VersionId", "")),
            "is_latest": v.get("IsLatest", True),
            "last_modified": v.get("LastModified", ""),
            "size": v.get("Size", ""),
            # 'storage_class': v.get('StorageClass'),
            "owner_name": v.get("Owner", {}).get("DisplayName", ""),
            "owner_id": v.get("Owner", {}).get("ID", ""),
            "anno": None,
        }
