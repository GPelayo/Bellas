from ..models import BellImage, BellGallery
from praw.models import Submission


class BaseArchiver:
    def __init__(self, gallery_name):
        self._gallery_name = gallery_name
        self.picture_data = None
        self.image_url = None
        self.thumb_url = None

    @property
    def gallery_name(self):
        return self._gallery_name

    @gallery_name.setter
    def gallery_name(self, name):
        self._gallery_name = name

    def load_image_db_data(self, picture_data: Submission, image_dir, thumb_dir=None):
        self.thumb_url = thumb_dir or image_dir
        self.image_url = image_dir
        self.picture_data = picture_data

    def save(self):
        raise NotImplemented

    def is_dupe_image(self, source_id):
        pass


class DjangoArchiver(BaseArchiver):
    pass


DEFAULT_IMG_WIDTH = 800
DEFAULT_IMG_HEIGHT = 1200


class DuplicateImageError(Exception):
    pass


class RedditImageArchiver(DjangoArchiver):
    def __init__(self, gallery_name):
        super().__init__(gallery_name)

    def is_dupe_image(self, source_id=None):
        sid = source_id or self.picture_data.id
        return BellImage.objects.filter(source_id=sid).exists()

    def load_image_db_data(self, picture_data: Submission, image_dir, thumb_dir=None):
        if self.is_dupe_image(source_id=picture_data.id):
            raise DuplicateImageError
        super().load_image_db_data(picture_data, image_dir, thumb_dir)

    def save(self):
        if BellGallery.objects.filter(name=self.gallery_name).exists():
            glry = BellGallery.objects.filter(name=self.gallery_name)[0]
        else:
            glry = BellGallery()
            glry.url = self.gallery_name.lower()
            glry.name = self.gallery_name.title()
            glry.save()

        if self.is_dupe_image(self.picture_data.id):
            img_obj = BellImage.objects.filter(self.picture_data.id)[0]
            # TODO add log above overriding image data
        else:
            img_obj = BellImage()
        img_obj.name = self.picture_data.title
        img_obj.source_id = self.picture_data.id
        img_obj.width = 800
        img_obj.height = 2000
        img_obj.image_location = self.image_url
        img_obj.thumbnail_location = self.thumb_url
        img_obj.parent_gallery = glry
        img_obj.save()
