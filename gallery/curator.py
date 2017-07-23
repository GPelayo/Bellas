from gallery.db.dao import WebGalleryDao
from gallery.gatherer.reddit import RedditGatherer, SubredditDoesntExistException
from gallery.media_storage.s3 import S3Apdater
from urllib.request import urlopen
from gallery.util import image as image_utils
from io import BytesIO

class BaseCurator:
    media_archiver = None
    db_archiver = None
    image_gatherer = None


ALLOWED_IMAGE_EXTENTIONS = ["jpg", "png", "gif", "bmp", "jpeg"]


class BellorumCurator(BaseCurator):
    def __init__(self, subreddit_name, gallery_name=None):
        self.media_archiver = S3Apdater()
        self.dao = WebGalleryDao()
        self.image_gatherer = RedditGatherer(subreddit_name,
                                             gallery_name=gallery_name,
                                             image_filter=self.image_filter(self.dao))

    def save_images(self, limit):
        self.image_filter("test")
        glry = self.image_gatherer.build_gallery(limit=limit)

        self.dao.save_gallery(glry)

        for img in glry.images:
            filename = img.source_url.split('/')[-1]
            img_buffer = BytesIO(urlopen(img.source_url).read())
            self.media_archiver.stream_to_storage(img_buffer, filename)
            img.width, img.height = image_utils.calc_image_size(img_buffer, filename=filename)
            img.image_url = img.thumb_url = self.media_archiver.get_url(filename)
            self.dao.save_image(img, glry)

        return glry.image_count

    @staticmethod
    def image_filter(image_dao):
        def validate_gathered_image(image_data):
            return image_data.source_url.split(".")[-1] in ALLOWED_IMAGE_EXTENTIONS \
                   and not image_dao.is_dupe_image(source_id=image_data.source_id)
        return validate_gathered_image