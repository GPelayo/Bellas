from gallery.contexts import ContextBuilder
from gallery.dj_rest_framework.dao import RestfulIndexDAO, RestfulPageDAO
from gallery.dj_rest_framework.serializers import IndexGallerySerializer, PageGallerySerializer


class IndexContextBuilder(ContextBuilder):
    def __init__(self):
        super().__init__()
        self.reader = PageGallerySerializer()

    def sync_wth_db(self):
        self.serial_model = RestfulIndexDAO().get_all_galleries()

    def build(self):
        srlzr = {'gallery': [IndexGallerySerializer(glry).data for glry in self.serial_model]}
        return srlzr


class PageContextBuilder(ContextBuilder):
    def __init__(self, gallery_id):
        super().__init__()
        self.reader = RestfulPageDAO(gallery_id)

    def sync_wth_db(self):
        self.serial_model = self.reader.get_gallery()

    def build(self):
        srlzr = PageGallerySerializer(self.serial_model)
        return srlzr.data
