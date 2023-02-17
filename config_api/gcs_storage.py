from google.cloud import storage
from django.core.files.storage import Storage


class GoogleCloudStorage(Storage):
    def __init__(self, client=None, bucket_name=None):
        self.client = client or storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def _open(self, name, mode='rb'):
        blob = self.bucket.blob(name)
        return blob.download_as_string()

    def _save(self, name, content):
        blob = self.bucket.blob(name)
        blob.upload_from_string(content)
        return name

    def url(self, name):
        blob = self.bucket.blob(name)
        return blob.public_url
