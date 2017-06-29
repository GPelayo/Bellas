from gallery.models import BellGallery, BellImage


class BaseDAO:
    pass


class WebGalleryDao(BaseDAO):
    @staticmethod
    def is_dupe_image(source_id):
        sid = source_id
        return BellImage.objects.filter(source_id=sid).exists()

    @staticmethod
    def save_gallery(gallery):
        glry = BellGallery()
        glry.name = gallery.name.lower()
        glry.description = gallery.description
        glry.save()

    @staticmethod
    def save_image(image, gallery):
        img_obj = BellImage()
        img_obj.name = image.name
        img_obj.source_id = image.source_id
        img_obj.width = image.width
        img_obj.height = image.height
        img_obj.image_location = image.image_url
        img_obj.thumbnail_location = image.thumb_url
        img_obj.parent_gallery = BellGallery.objects.get(name=gallery.name.lower())
        img_obj.save()
