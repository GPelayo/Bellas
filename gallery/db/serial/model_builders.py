from typing import List

from gallery.db.serial import models
from gallery.models import BellImage, BellGallery


class SerialModelBuilder:
    pass


class SerialIndexGalleryBuilder(SerialModelBuilder):
    def __init__(self, db_gallery: BellGallery, preview_image: BellImage):
        self.db_gallery = db_gallery
        self.preview_image = preview_image

    def create(self):
        serial_mdl = models.SerialIndexGallery()
        serial_mdl.name = self.db_gallery.name
        serial_mdl.slug = self.db_gallery.pk
        serial_mdl.description = self.db_gallery.description
        serial_mdl.preview_image_url = self.preview_image.thumbnail_location

        return serial_mdl


class SerialPageImageBuilder(SerialModelBuilder):
    def __init__(self, db_image: BellImage):
        self.db_image = db_image

    def create(self):
        serial_mdl = models.SerialPageImage()
        serial_mdl.name = self.db_image.name
        serial_mdl.image_url = self.db_image.image_location
        serial_mdl.thumb_url = self.db_image.thumbnail_location
        serial_mdl.height = self.db_image.height
        serial_mdl.width = self.db_image.width
        return serial_mdl


class SerialPageGalleryBuilder(SerialModelBuilder):
    def __init__(self, db_gallery: BellGallery, image_list: List[BellImage]):
        self.db_gallery = db_gallery
        self.image_list = image_list

    def create(self):
        serial_mdl = models.SerialIndexGallery()
        serial_mdl.name = self.db_gallery.name
        serial_mdl.description = self.db_gallery.description
        serial_mdl.images = [SerialPageImageBuilder(img).create() for img in self.image_list]
        return serial_mdl
