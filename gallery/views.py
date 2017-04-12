from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from gallery.models import BellGallery, BellImage
from gallery.serializers import BellGallerySerializer, BellImageSerializer
from bellorum.settings import MEDIA_URL

APP_NAME = "gallery"


def gallery_list(request):
    if request.method == 'GET':
        all_gall = BellGallery.objects.all()
        srlzr = BellGallerySerializer(all_gall, many=True)
        return JsonResponse(srlzr.data, safe=False)


def gallery_data(request):
    if request.method == 'GET':
        gallery_name = request.GET['name']
        with_images = True if request.GET.get('with_images', "False").lower() == "true" else False
        glry = BellGallery.objects.get(name=gallery_name)
        json_data = BellGallerySerializer(glry).data
        media_prefix = "{}{}".format(MEDIA_URL[1:], APP_NAME)
        json_data.update({"media_root": media_prefix})
        if with_images:
            images = BellImage.objects.filter(parent_gallery=glry)
            json_data.update({"images": BellImageSerializer(images, many=True).data})

        return JsonResponse(json_data, safe=False)

