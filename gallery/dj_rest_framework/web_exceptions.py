from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class WrongGalleryException(APIException):
    status_code = 400
    default_detail = "Gallery doesn't exist. Please check the id/name."
    default_code = 'bad_request'

    def __init__(self, gallery_id):
        self.detail = "Gallery doesn't exist. Please check the id/name.".format(gallery_id)


def bell_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response:
        response.data['status_code'] = response.status_code

    return response
