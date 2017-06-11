from django.test import TestCase
from gallery.media_storage import s3
from urllib import request
from gallery.tasks import gather_pictures
from gallery.util import images


class S3TestCase(TestCase):
    def setUp(self):
        pass

    def test_save_image(self):
        adptr = s3.S3Apdater()
        test_img_resp = request.urlopen("https://bellorum.s3.amazonaws.com/SbK9fZD.jpg")
        adptr.save_chucks(test_img_resp, 'test-folder/tests.jpg')
        assert True


class GatherTestCase(TestCase):
    def test_gather_pictures_task(self):
        gather_pictures('roomporn', name='room')


class ImageUtilTests(TestCase):
    def test_calc_image_size(self):
        test_image_filename = 'test-folder/tests.jpg'
        test_image_source = 'https://bellorum.s3.amazonaws.com:443/'
        test_width, test_height = 2048, 1365
        img_width, img_height = images.calc_image_size(test_image_source, test_image_filename)

        self.assertEqual(test_width, img_width)
        self.assertEqual(test_height, img_height)
