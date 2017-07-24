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
        tg2.description = 'Single Image Gallery 2'
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

        self.galleries = [tg, tg2]
        self.single_image_gallery = tg2
        self.multi_image_gallery = tg
        self.multi_image_gallery_images = [ti, ti2]
        self.single_image_gallery_images = [ti3]

    def check_index(self, test_case: TestCase, response):
        exp_gallery_list = json.loads(response.content.decode('utf-8'))
        valid_gallery_list = {
            self.galleries[0].name: {
                'name': self.galleries[0].name,
                'slug': str(self.galleries[0].pk),
                'description': self.galleries[0].description,
                'preview_image_url': self.multi_image_gallery_images[-1].thumbnail_location
            },
            self.galleries[1].name: {
                'name': self.galleries[1].name,
                'slug': str(self.galleries[1].pk),
                'description': self.galleries[1].description,
                'preview_image_url': self.single_image_gallery_images[-1].thumbnail_location
            }
        }

        test_case.assertEqual(len(exp_gallery_list['gallery']), len(valid_gallery_list), msg='Wrong Gallery Count')

        for g in exp_gallery_list['gallery']:
            valid_data = valid_gallery_list[g['name']]
            test_case.assertEqual(valid_data['name'], g['name'], msg='Wrong Gallery Name')
            test_case.assertEqual(valid_data['slug'], g['slug'], msg='Wrong Gallery Slug')
            test_case.assertEqual(valid_data['description'], g['description'], msg='Wrong Gallery Description')
            test_case.assertEqual(valid_data['preview_image_url'], g['preview_image_url'], msg='Wrong Preview Url')

    def check_image_gallery(self, test_case: TestCase, response):
        exp_gallery = json.loads(response.content.decode('utf-8'))

        valid_gallery = {
            'name': self.single_image_gallery.name,
            'description': self.single_image_gallery.description,
            'images': {
                img.pk: {
                    'name': img.name,
                    'image_url': img.image_location,
                    'thumb_url': img.thumbnail_location,
                    'width': img.width,
                    'height': img.height
                } for img in self.single_image_gallery_images
            }
        }
        test_case.assertEqual(exp_gallery['name'], valid_gallery['name'], msg='Wrong Gallery Name')
        test_case.assertEqual(exp_gallery['description'], valid_gallery['description'], msg='Wrong Gallery Description')
        test_case.assertEqual(len(exp_gallery['images']), len(valid_gallery['images']), msg='Wrong Image Count')
        # test_case.assertEqual(len(exp_gallery['gallery']), len(valid_gallery), msg='Wrong Gallery Count')
        #
        # for g in exp_gallery['images']:
        #     valid_data = valid_gallery[g['name']]
        #     test_case.assertEqual(valid_data['name'], g['name'], msg='Wrong Gallery Name')
        #     test_case.assertEqual(valid_data['slug'], g['slug'], msg='Wrong Gallery Slug')
        #     test_case.assertEqual(valid_data['description'], g['description'], msg='Wrong Gallery Description')
        #     test_case.assertEqual(valid_data['preview_image_url'], g['preview_image_url'], msg='Wrong Preview Url')


class APITestCase(TestCase):
    def setUp(self):
        self.db_tester = TestDBEntries()
        self.index_url = dj_urls.reverse(INDEX_VIEW_NAME)
        self.single_img_gallery_url = dj_urls.reverse(GALLERY_VIEW_NAME,
                                                      args=[str(self.db_tester.single_image_gallery.pk)])
        self.client = Client()

    def test_index(self):
        resp = self.client.get(self.index_url)
        self.db_tester.check_index(self, resp)

    def test_single_image_gallery(self):
        resp = self.client.get(self.single_img_gallery_url)
        self.db_tester.check_image_gallery(self, resp)


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
