from .db.dao import IndexDAO, GridDAO


class ContextBuilder:
    context = None
    reader = None

    def __init__(self):
        self.context = {}

    def sync_wth_db(self):
        raise NotImplemented


class IndexContextBuilder(ContextBuilder):
    def sync_wth_db(self):
        self.context['gallery_list'] = IndexDAO().get_all_galleries()


class Image:
    name = None
    description = None
    image_url = None
    thumb_url = None
    dimensions = None
    tags = None


MAX_IMAGE_PER_GALLERY = 100


class GridContextBuilder(ContextBuilder):
    gallery_name = None

    def __init__(self, gallery_id):
        super().__init__()
        self.reader = GridDAO(gallery_id, image_qty_per_sync=MAX_IMAGE_PER_GALLERY)

    def sync_wth_db(self):
        self.context['gallery_name'] = self.reader.gallery_name
        self.context['image_list'] = self.reader.get_images()
