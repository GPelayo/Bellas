from ..models import BellGallery, BellImage


class BaseDBModelFactory:
    query_obj = None


class GalleryDBModel:
    url = None
    name = None
    images = None
    description = None

    def __init__(self):
        self.images = []

    def add_image(self, image):
        self.images.append(image)

    def add_image_list(self, image_list):
        for img in image_list:
            self.images.append(img)

    def __str__(self):
        return str((self.url, self.name, self.images))


class GalleryDBModelFactory(BaseDBModelFactory):
    def __init__(self, query_object: BellGallery):
        self.query_obj = query_object

    def create(self):
        g_obj = GalleryDBModel()
        g_obj.name = self.query_obj.name
        g_obj.url = str(self.query_obj.id)
        g_obj.description = self.query_obj.description or ''
        g_obj.images = GridDAO(self.query_obj.id, image_qty_per_sync=5).get_images()
        return g_obj


class BaseDAO:
    pass


class IndexDAO(BaseDAO):
    @staticmethod
    def get_all_galleries():
        return [GalleryDBModelFactory(glry).create() for glry in BellGallery.objects.all()]


class ImageDBModel:
    name = None
    description = None
    image_url = None
    thumb_url = None
    dimensions = None
    tags = None


class ImageDBModelFactory(BaseDBModelFactory):
    def __init__(self, query_object: BellImage):
        self.query_obj = query_object

    def create(self):
        img_obj = ImageDBModel()
        img_obj.name = self.query_obj.name
        img_obj.image_url = self.query_obj.image_location
        img_obj.thumb_url = self.query_obj.thumbnail_location
        img_obj.dimensions = "{}x{}".format(self.query_obj.width,
                                            self.query_obj.height)
        return img_obj


class GridDAO(BaseDAO):
    def __init__(self, gallery_id, image_qty_per_sync=10):
        self.gallery_id = gallery_id
        self.image_qty = image_qty_per_sync

    def get_images(self):
        return [ImageDBModelFactory(img).create()
                for img in BellImage.objects.filter(parent_gallery__pk=self.gallery_id)[: self.image_qty]]

    @property
    def gallery_name(self):
        return BellGallery.objects.get(pk=self.gallery_id).name

    def get_gallery(self):
        glry = BellGallery.objects.get(pk=self.gallery_id)
        return GalleryDBModelFactory(glry).create()
