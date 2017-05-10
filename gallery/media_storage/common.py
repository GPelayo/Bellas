from django.core.files.storage import default_storage
CHUNK_SIZE = 16 * 1024


class StorageAdapter:
    storage = default_storage

    def save_chucks(self, response, filename):
        fl = self.storage.open(filename, 'w')
        while True:
            chunk = response.read(CHUNK_SIZE)
            fl.write(chunk)
            if not chunk:
                break
        fl.close()
