from urllib import request, parse
from io import BytesIO
import json
from django import urls as dj_urls
from django.test import TestCase, Client
from bellas import settings, urls
from gallery.media_storage import s3
from gallery.models import BellGallery, BellImage
from gallery.util import image
from gallery.tasks import gather_pictures

TEST_IMAGE_URL = 'https://s3-us-west-1.amazonaws.com/bellorum/test-folder/tests.jpg'
BUCKET_TEST_FOLDER_PATH = 'test-folder/tests.jpg'
TEST_GALLERY_NAME = "accidental renaissance"
TEST_SUBREDDIT_NAME = "accidentalrenaissance"

INDEX_VIEW_NAME = 'index'
GALLERY_VIEW_NAME = 'galleries'


class TestDBEntries:
    def __init__(self):
        tg = BellGallery()
        tg.name = 'Multi Image Gallery'
        tg.description = 'Multi Image Gallery Description'
        tg.save()
        ti = BellImage()
        ti.name = 'Test Image'
        ti.width = '1212'
        ti.source_id = "1"
        ti.height = '8989'
        ti.image_location = 'https://www.fakeimagestorage.com/fakeimg.jpg'
        ti.thumbnail_location = 'https://www.fakeimagestorage.com/fakethumbnail.jpg'
        ti.parent_gallery = tg
        ti.save()
        ti2 = BellImage()
        ti2.name = 'Test Image 2'
        ti2.width = '2323'
        ti2.height = '7878'
        ti2.source_id = "2"
        ti2.image_location = 'https://www.fakeimagestorage.com/fakeimg2.jpg'
        ti2.thumbnail_location = 'https://www.fakeimagestorage.com/fakethumbnail2.jpg'
        ti2.parent_gallery = tg
        ti2.save()
        tg2 = BellGallery()

        tg2.name = 'Single Image Gallery'
        tg2.description = 'Single Image Gallery'
        tg2.save()
        ti3 = BellImage()
        ti3.name = 'Test Image 3'
        ti3.width = '2323'
        ti3.height = '7878'
        ti3.source_id = "3"
        ti3.image_location = 'https://www.fakeimagestorage.com/fakeimg2.jpg'
        ti3.thumbnail_location = 'https://www.fakeimagestorage.com/fakethumbnail3.jpg'
        ti3.parent_gallery = tg2
        ti3.save()

        tg3 = BellGallery()
        tg3.name = 'Blank Image Gallery'
        tg3.description = 'Blank Image Gallery'
        tg3.save()

        self.multi_image_gallery_data = self.generate_gallery_serial(tg, [ti, ti2])
        self.single_image_gallery_data = self.generate_gallery_serial(tg2, [ti3])
        self.no_image_gallery_data = self.generate_gallery_serial(tg3, [])
        self.galleries = [self.multi_image_gallery_data,
                          self.single_image_gallery_data,
                          self.no_image_gallery_data]

    @staticmethod
    def generate_gallery_serial(gallery, images):
        return {
            'id': gallery.pk,
            'name': gallery.name,
            'description': gallery.description,
            'preview_image_url': images[-1].thumbnail_location if len(images) > 0 else None,
            'images': {
                img.pk: {
                    'name': img.name,
                    'image_url': img.image_location,
                    'thumb_url': img.thumbnail_location,
                    'width': img.width,
                    'height': img.height
                } for img in images
            }
        }

    def check_index(self, test_case: TestCase, response):
        exp_glry_data = json.loads(response.content.decode('utf-8'))
        exp_glry_list = exp_glry_data['gallery']

        valid_gallery_list = {
            g['name']: {
                'name': g['name'],
                'slug': str(g['id']),
                'description': g['description'],
                'preview_image_url': g['preview_image_url']
            } for g in self.galleries
         }
        test_case.assertEqual(len(exp_glry_list), len(valid_gallery_list), msg='Wrong Gallery Count')

        for g in exp_glry_list:
            valid_data = valid_gallery_list[g['name']]
            test_case.assertEqual(valid_data['name'], g['name'], msg='Wrong Gallery Name')
            test_case.assertEqual(valid_data['slug'], g['slug'], msg='Wrong Gallery Slug')
            test_case.assertEqual(valid_data['description'], g['description'], msg='Wrong Gallery Description')
            test_case.assertEqual(valid_data['preview_image_url'], g['preview_image_url'], msg='Wrong Preview Url')

    def check_empty_gallery(self, test_case: TestCase, response):
        self._check_image_gallery(test_case, response, self.no_image_gallery_data)

    def check_single_image_gallery(self, test_case: TestCase, response):
        self._check_image_gallery(test_case, response, self.single_image_gallery_data)

    def check_multi_image_gallery(self, test_case: TestCase, response):
        self._check_image_gallery(test_case, response, self.multi_image_gallery_data)

    @staticmethod
    def _check_image_gallery(test_case: TestCase, response, valid_gallery_data):
        exp_gallery = json.loads(response.content.decode('utf-8'))
        test_case.assertEqual(exp_gallery['name'], valid_gallery_data['name'], msg='Wrong Gallery Name')
        test_case.assertEqual(exp_gallery['description'], valid_gallery_data['description'], msg='Wrong Gallery Description')
        test_case.assertEqual(len(exp_gallery['images']), len(valid_gallery_data['images']), msg='Wrong Image Count')


class APITestCase(TestCase):
    def setUp(self):
        self.db_tester = TestDBEntries()
        self.index_url = dj_urls.reverse(INDEX_VIEW_NAME)

        self.client = Client()

    def test_index(self):
        resp = self.client.get(self.index_url)
        self.db_tester.check_index(self, resp)

    def test_gallery(self):
        self.normal_gallery_url = dj_urls.reverse(GALLERY_VIEW_NAME,
                                                  args=[str(self.db_tester.multi_image_gallery_data['id'])])
        resp = self.client.get(self.normal_gallery_url)
        self.db_tester.check_multi_image_gallery(self, resp)

    def test_single_image_gallery(self):
        self.single_img_gallery_url = dj_urls.reverse(GALLERY_VIEW_NAME,
                                                      args=[str(self.db_tester.single_image_gallery_data['id'])])
        resp = self.client.get(self.single_img_gallery_url)
        self.db_tester.check_single_image_gallery(self, resp)

    def test_empty_gallery(self):
        self.no_img_gallery_url = dj_urls.reverse(GALLERY_VIEW_NAME,
                                                  args=[str(self.db_tester.no_image_gallery_data['id'])])
        resp = self.client.get(self.no_img_gallery_url)
        self.db_tester.check_empty_gallery(self, resp)


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
