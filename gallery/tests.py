from django.test import TestCase
from bellas import settings
from gallery.media_storage import s3
from urllib import request, parse
from gallery.tasks import gather_pictures
from gallery.util import image
from io import BytesIO

TEST_IMAGE_URL = 'https://s3-us-west-1.amazonaws.com/bellorum/test-folder/tests.jpg'
BUCKET_TEST_FOLDER_PATH = 'test-folder/tests.jpg'
TEST_GALLERY_NAME = "accidental renaissance"
TEST_SUBREDDIT_NAME = "accidentalrenaissance"


class S3TestCase(TestCase):
    def setUp(self):
        pass

    def test_save_image(self):
        adptr = s3.S3Apdater()
        test_img_buffer = BytesIO(request.urlopen(TEST_IMAGE_URL).read())
        adptr.save_chucks(test_img_buffer, BUCKET_TEST_FOLDER_PATH)


class GatherTestCase(TestCase):
    def test_gather_pictures_task(self):
        gather_pictures(TEST_SUBREDDIT_NAME, name=TEST_GALLERY_NAME)


class ImageUtilTests(TestCase):
    def test_calc_image_size(self):
        s3_bucket_url = 'https://{}.s3.amazonaws.com:443/'.format(settings.AWS_STORAGE_BUCKET_NAME)
        test_folder_url = parse.urljoin(s3_bucket_url, BUCKET_TEST_FOLDER_PATH)
        test_image_buffer = BytesIO(request.urlopen(test_folder_url).read())
        test_width, test_height = 2048, 1365
        img_width, img_height = image.calc_image_size(test_image_buffer, BUCKET_TEST_FOLDER_PATH)

        self.assertEqual(test_width, img_width)
        self.assertEqual(test_height, img_height)
