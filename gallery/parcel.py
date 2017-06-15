class Parcel:
    pass


class DBParcelBuilder:
    query_obj = None


class ImageDBModel:
    name = None
    description = None
    image_url = None
    thumb_url = None
    dimensions = None
    tags = None


class WebImageParcel(ImageDBModel):
    source_id = None
    source_url = None
    width = None
    height = None
    parent_gallery = None


class ImageDBModelBuilder(DBParcelBuilder):
    def __init__(self, query_object):
        self.query_obj = query_object

    def create(self):
        img_obj = ImageDBModel()
        img_obj.name = self.query_obj.name
        img_obj.image_url = self.query_obj.image_location
        img_obj.thumb_url = self.query_obj.thumbnail_location
        img_obj.dimensions = "{}x{}".format(self.query_obj.width,
                                            self.query_obj.height)
        return img_obj


class GalleryParcel:
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

    @property
    def image_count(self):
        return len(self.images)

    def __str__(self):
        return str((self.url, self.name, self.images))


class GalleryDBParcelBuilder(DBParcelBuilder):
    def __init__(self, query_object, images):
        self.query_obj = query_object
        self.images = images

    def create(self):
        g_obj = GalleryParcel()
        g_obj.name = self.query_obj.name
        g_obj.url = str(self.query_obj.id)
        g_obj.description = self.query_obj.description or ''
        g_obj.images = self.images
        return g_obj