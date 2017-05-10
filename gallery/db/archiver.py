from ..models import BellImage, BellGallery
from gallery.logger import BellLogger
from praw.models import Submission
import imghdr
import struct
import os


DEFAULT_IMG_WIDTH = 800
DEFAULT_IMG_HEIGHT = 1200

imgerr_log = BellLogger("image_sizer", default_level="INFO")


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
        # self.width, self.height = self.__calc_image_size() or (DEFAULT_IMG_WIDTH, DEFAULT_IMG_HEIGHT)
        self.width, self.height = 800, 800

    def save(self):
        raise NotImplemented

    def is_dupe_image(self, source_id):
        pass

    def __calc_image_size(self):
        full_path = os.path.join(self.media_folder, self.image_filepath)
        with open(full_path, 'rb') as fhandle:
            head = fhandle.read(24)
            if len(head) != 24:
                imgerr_log.log("Error Short head < 24: {}".format(self.image_filepath))
                return
            if imghdr.what(full_path) == 'png':
                check = struct.unpack('>i', head[4:8])[0]
                if check != 0x0d0a1a0a:
                    imgerr_log.log("Error PNG 0x0d0a1a0a: {}".format(self.image_filepath))
                    return
                width, height = struct.unpack('>ii', head[16:24])
            elif imghdr.what(full_path) == 'gif':
                width, height = struct.unpack('<HH', head[6:10])
            else:
                try:
                    fhandle.seek(0)  # Read 0xff next
                    size = 2
                    ftype = 0
                    while not 0xc0 <= ftype <= 0xcf:
                        fhandle.seek(size, 1)
                        byte = fhandle.read(1)
                        while ord(byte) == 0xff:
                            byte = fhandle.read(1)
                        ftype = ord(byte)
                        size = struct.unpack('>H', fhandle.read(2))[0] - 2
                    # We are at a SOFn block
                    fhandle.seek(1, 1)  # Skip `precision' byte.
                    height, width = struct.unpack('>HH', fhandle.read(4))
                except Exception as e:
                    imgerr_log.log("Error W0703: {}, {}".format(self.image_filepath, str(e)))
                    return
            imgerr_log.log("{}: {}x{}".format(self.image_filepath, self.width, self.height))

            width = width if width > 20 else DEFAULT_IMG_WIDTH
            height = height if height > 20 else DEFAULT_IMG_HEIGHT
        return width, height


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
