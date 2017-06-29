from django.test import TestCase
from gallery.media_storage import s3
from urllib import request, parse
from gallery.tasks import gather_pictures
from gallery.util import image
from io import BytesIO


class S3TestCase(TestCase):
    def setUp(self):
        pass

    def test_save_image(self):
        adptr = s3.S3Apdater()
        test_img_buffer = BytesIO(request.urlopen("https://bellorum.s3.amazonaws.com/SbK9fZD.jpg").read())
        adptr.save_chucks(test_img_buffer, 'test-folder/tests.jpg')
        assert True


class GatherTestCase(TestCase):
    def test_gather_pictures_task(self):
        gather_pictures('pics')

    def test_gallery_name_case(self):
        gather_pictures('CozyPlaces', name='Cozy Places')

    def test_url_error(self):
        gather_pictures('bellorum_dev_bug_urls')


class ImageUtilTests(TestCase):
    def test_calc_image_size(self):
        test_image_filename = 'test-folder/tests.jpg'
        test_image_buffer = BytesIO(request.urlopen(parse.urljoin('https://bellorum.s3.amazonaws.com:443/',
                                                   test_image_filename)).read())
        test_width, test_height = 2048, 1365
        img_width, img_height = image.calc_image_size(test_image_buffer, test_image_filename)

        self.assertEqual(test_width, img_width)
        self.assertEqual(test_height, img_height)
