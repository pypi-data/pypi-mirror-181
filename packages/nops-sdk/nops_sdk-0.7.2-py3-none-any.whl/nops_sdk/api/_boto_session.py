from __future__ import annotations

import os

import boto3


def get_boto_session() -> boto3.Session:
    if AWS_PROFILE := os.environ.get("NOPS_AWS_PROFILE"):
        boto_session = boto3.Session(profile_name=AWS_PROFILE)
    else:
        boto_session = boto3.Session()
    return boto_session
