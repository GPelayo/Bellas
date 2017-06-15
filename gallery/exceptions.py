class BellException(Exception):
    error_code = None


class NonexistentGalleryError(BellException):
    error_code = 400

    def __init__(self, gallery_id):
        message = "Gallery ({}) is Missing/Nonexistent".format(gallery_id)
        super().__init__(message)


class DuplicateImageError(Exception):
    pass
