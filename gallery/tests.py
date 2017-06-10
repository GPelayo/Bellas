from django.test import TestCase
from gallery.media_storage import s3
from urllib import request
from gallery.tasks import gather_pictures


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
