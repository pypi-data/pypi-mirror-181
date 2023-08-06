import io
import os
import pandas as pd

import cloudfiles.connections as conn
from cloudfiles.logger import *

"""
Useful stuff:
JSON schemas: https://specs.frictionlessdata.io/table-schema/#types-and-formats
"""


class FileHelper:
    def __init__(self, bucket_name: str = None, logger: Logger = None, environment: str = None):
        self.environment = environment if environment else os.getenv("ENVIRONMENT", "dev")
        self.bucket_name = bucket_name if bucket_name else self.environment
        self.logger = logger if logger else Logger()

    # Get path for s3fs
    def fspath(self, path: str):
        return f"{self.bucket_name}/{path}"

    # Move file
    def move(self, path_from: str, path_to: str, recursive: bool = False):
        conn.fs.move(self.fspath(path_from), self.fspath(path_to), recursive=recursive)

    # Copy file
    def copy(self, path_from: str, path_to: str, recursive: bool = False):
        conn.fs.copy(self.fspath(path_from), self.fspath(path_to), recursive=recursive)

    # Delete file
    def delete(self, path: str, recursive: str = False):
        conn.fs.rm(self, self.fspath(path), recursive=recursive)

    # Get a readable file object
    def get_readable(self, path: str):
        return conn.fs.open(self.fspath(path))

    # Get a writeable file object
    def get_writeable(self, path: str):
        return conn.fs.open(self.fspath(path), "w")

    # Download a file into a ByteIO object
    def read_byteio(self, path: str):
        output = io.BytesIO()
        conn.boto.Bucket(self.bucket_name).download_fileobj(Key=path, Fileobj=output)
        return output

    # Download file content as bytes
    def read_bytes(self, path: str):
        output = self.read_byteio(path)
        return output.getvalue()

    # Upload bytes into a file
    def write_bytes(self, path: str, data: bytes):
        self.logger.info(f"[{self.bucket_name}] Uploading bytes to {path}")
        result = conn.boto.Bucket(self.bucket_name).put_object(Key=path, Body=data)
        return result

    # Download file content as text
    def read_text(self, path: str, encoding: str = "utf8"):
        byte_content = self.read_bytes(path)
        return byte_content.decode(encoding)

    # Upload text into a file
    def write_text(self, path: str, text: str, encoding: str = "utf8"):
        self.logger.info(f"[{self.bucket_name}] Uploading text to {path}")
        result = conn.boto.Bucket(self.bucket_name).put_object(Key=path, Body=text.encode(encoding))
        return result

    # Read a JSON file into a Pandas DataFrame
    def read_json(self, path: str, **kwargs):
        return pd.read_json(self.get_readable(path), **kwargs)

    # Write to a JSON file
    def write_json(self, path: str, df: pd.DataFrame, **kwargs):
        return df.to_json(self.get_writeable(path), **kwargs)

    # Read a Parquet file into a Pandas DataFrame
    def read_parquet(self, path: str, **kwargs):
        return pd.read_parquet(self.get_readable(path), **kwargs)

    # Write to a parquet file
    def write_parquet(self, path: str, df: pd.DataFrame, **kwargs):
        return df.to_parquet(self.get_writeable(path), **kwargs)
