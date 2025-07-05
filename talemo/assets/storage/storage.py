"""
Custom storage class for asset storage.
"""
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class CustomS3Boto3Storage(S3Boto3Storage):
    """
    Storage class for S3/MinIO assets.
    """
    pass