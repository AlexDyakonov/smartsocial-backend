from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN

    def url(self, name, parameters=None, expire=None, http_method=None):
        if self.custom_domain:
            return f"https://{self.custom_domain}/media/{name}"
        return super().url(name, parameters, expire, http_method)
