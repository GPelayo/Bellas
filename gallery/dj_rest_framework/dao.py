from gallery.db.dao import BaseDAO
from gallery.db.parcel.builders import IndexGalleryParcelBuilder, PageGalleryParcelBuilder
from gallery.models import BellImage, BellGallery
from django.core.exceptions import ObjectDoesNotExist
from gallery.exceptions import NonexistentGalleryError


class RestfulIndexDAO(BaseDAO):
    def get_all_galleries(self):
        output_galleries = []
        for mdl in BellGallery.objects.all():
            prv_img = BellImage.objects.filter(parent_gallery=mdl.pk)[0]
            sr_mdl = IndexGalleryParcelBuilder(mdl, prv_img).create()
            output_galleries.append(sr_mdl)
        return output_galleries


class RestfulPageDAO(BaseDAO):
    def __init__(self, gallery_id, image_qty_per_sync=10):
        self.gallery_id = gallery_id
        self.image_qty = image_qty_per_sync

    def get_gallery(self):
        try:
            gallery = BellGallery.objects.get(id=self.gallery_id)
        except ObjectDoesNotExist:
            raise NonexistentGalleryError(self.gallery_id)
        else:
            image_list = BellImage.objects.filter(parent_gallery=self.gallery_id)
            return PageGalleryParcelBuilder(gallery, image_list).create()
