class Parcel:
    pass


class IndexGalleryParcel(Parcel):
    name = None
    slug = None
    description = None
    preview_image_url = None


class ImageParcel(Parcel):
    name = None
    image_url = None
    thumb_url = None
    dimensions = None


class GalleryParcel(Parcel):
    name = None
    description = None
    images = None

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
        return str((self.name, self.images))


class WebImageParcel(ImageParcel):
    source_id = None
    source_url = None
    width = None
    height = None
    parent_gallery = None
