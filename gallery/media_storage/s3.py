from gallery.media_storage.common import StorageAdapter
from django.core.files.storage import default_storage


class S3Apdater(StorageAdapter):
    def __init__(self, storage=default_storage):
        self.storage = storage

    def save_chucks(self, response, filename):
        return super().save_chucks(response, filename)

    def stream_to_storage(self, file_response, filename):
        self.save_chucks(file_response, filename)

    def get_url(self, filename):
        return self.storage.url(filename)