from gallery.models import BellImage, BellGallery
from gallery.util import images
from praw.models import Submission


class BaseArchiver:
    def __init__(self, gallery_name, media_folder):
        self._gallery_name = gallery_name.lower()
        self.description = None
        self.image_data = None
        self.image_filepath = None
        self.thumb_filepath = None
        self.media_folder = media_folder
        self.height = self.width = None

    @property
    def gallery_name(self):
        return self._gallery_name

    @gallery_name.setter
    def gallery_name(self, name):
        self._gallery_name = name

    def load_image_db_data(self, picture_data: Submission, image_dir, thumb_dir=None):
        self.thumb_filepath = thumb_dir or image_dir
        self.image_filepath = image_dir
        self.image_data = picture_data
        self.width, self.height = images.calc_image_size(self.media_folder, self.image_filepath) or \
                                  (images.DEFAULT_IMG_WIDTH, images.DEFAULT_IMG_HEIGHT)

    def save(self):
        raise NotImplemented

    def is_dupe_image(self, source_id):
        pass




class DjangoArchiver(BaseArchiver):
    pass


class DuplicateImageError(Exception):
    pass


class RedditImageArchiver(DjangoArchiver):
    def __init__(self, subreddit, media_root):
        super().__init__(subreddit, media_root)

    def is_dupe_image(self, source_id=None):
        sid = source_id or self.image_data.id
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
            glry.name = self.gallery_name.lower()
            glry.description = self.description
            glry.save()

        if self.is_dupe_image(self.image_data.id):
            img_obj = BellImage.objects.filter(self.image_data.id)[0]
            # TODO add log above overriding image data
        else:
            img_obj = BellImage()
        img_obj.name = self.image_data.title
        img_obj.source_id = self.image_data.id
        img_obj.width = self.width
        img_obj.height = self.height
        img_obj.image_location = self.image_filepath
        img_obj.thumbnail_location = self.thumb_filepath
        img_obj.parent_gallery = glry
        img_obj.save()
