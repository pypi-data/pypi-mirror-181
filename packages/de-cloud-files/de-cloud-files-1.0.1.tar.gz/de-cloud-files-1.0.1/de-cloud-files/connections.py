import boto3
import s3fs

"""
Connections to different services

boto: Boto3 resource for s3/minio - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#using-boto3
fs: s3fs File System for s3/minio - https://s3fs.readthedocs.io/en/latest/api.html#s3fs.core.S3FileSystem
"""

s3fs_config = {
    "anon": False,
    "client_kwargs": {
        "endpoint_url": None,
        "aws_access_key_id": None,
        "aws_secret_access_key": None,
        "aws_session_token": None
    },
    "config_kwargs": {
        'signature_version': 's3v4'
    }
}

boto3_config = {
    "service_name": "s3",
    "endpoint_url": None,
    "aws_access_key_id": None,
    "aws_secret_access_key": None,
    "aws_session_token": None,
    "config": boto3.session.Config(signature_version='s3v4'),
    "verify": True
}

fs = None
boto = None


def connect_s3(**kwargs):
    global fs, boto

    for key, value in kwargs.items():
        boto3_config[key] = value
        s3fs_config["client_kwargs"][key] = value

    fs = s3fs.S3FileSystem(**s3fs_config)
    boto = boto3.resource(**boto3_config)
