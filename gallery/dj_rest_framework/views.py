from gallery.dj_rest_framework.contexts import IndexContextBuilder, PageContextBuilder
from gallery.dj_rest_framework.web_exceptions import WrongGalleryException
from gallery.exceptions import NonexistentGalleryError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny
from django.http import response
from bellas.settings import README_LINK


class IndexView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        bldr = IndexContextBuilder()
        bldr.sync_wth_db()
        return Response(bldr.build())


class PageView(APIView):
    renderer_classes = (JSONRenderer, )
    permission_classes = (AllowAny, )

    def get(self, request, gallery_id, format=None):
        bldr = PageContextBuilder(gallery_id)
        try:
            bldr.sync_wth_db()
        except NonexistentGalleryError:
            raise WrongGalleryException(gallery_id)
        else:
            return Response(bldr.build())


def landing_page(request):
    html = "<h2>Welcome to Bellapi!</h2>" \
           "<p>If you want to learn how to use this API, please checkout the " \
           "<a href='{}'>Readme</a>.</p>".format(README_LINK)

    return response.HttpResponse(html)
