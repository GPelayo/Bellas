from .db.dao import MenuDAO, GridDAO


class ContextBuilder:
    context = None
    reader = None

    def __init__(self):
        self.context = {}
        self.sync_wth_db()

    def sync_wth_db(self):
        raise NotImplemented


# TODO change to withMenu decorator
class WithMenuContextBuilder(ContextBuilder):
    def sync_wth_db(self):
        rdr = MenuDAO()
        glr = rdr.get_all_galleries()
        self.context['gallery_list'] = rdr.get_all_galleries()


class IndexContextBuilder(WithMenuContextBuilder):
    def sync_wth_db(self):

        super().sync_wth_db()


class Image:
    name = None
    description = None
    image_url = None
    thumb_url = None
    dimensions = None
    tags = None


class GridContextBuilder(WithMenuContextBuilder):
    gallery_name = None

    def __init__(self, gallery_name):
        super().__init__()
        self.reader = GridDAO(gallery_name)
        self.gallery_name = gallery_name
        self.sync_wth_db()

    def sync_wth_db(self):
        super().sync_wth_db()
        if self.gallery_name:
            self.context['gallery_name'] = self.gallery_name
            self.context['image_list'] = self.reader.get_images()
