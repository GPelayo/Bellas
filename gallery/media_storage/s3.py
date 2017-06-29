from gallery.media_storage.common import StorageAdapter
from bellorum.settings import AWS_STORAGE_GALLERY_FOLDER, SERVER_LOCATION
from django.core.files.storage import default_storage


class S3Apdater(StorageAdapter):
    def __init__(self, storage=default_storage):
        self.storage = storage

    def save_chucks(self, image_buffer, filename, gallery_name):
        full_file_path = self.create_full_dir_path(filename, gallery_name)
        image_buffer.seek(0)
        return super().save_chucks(image_buffer, full_file_path, gallery_name)

    def stream_to_storage(self, file_response, filename, gallery_name):
        self.save_chucks(file_response, filename, gallery_name)

    def get_url(self, filename, gallery_name):
        full_path = self.create_full_dir_path(filename, gallery_name)
        return self.storage.url(full_path)

    @staticmethod
    def create_full_dir_path(filename, gallery_name):
        return "{}/{}/{}/{}".format(AWS_STORAGE_GALLERY_FOLDER, SERVER_LOCATION,
                             gallery_name, filename)
