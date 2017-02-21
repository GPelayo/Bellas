from django.shortcuts import render


class Image:
    name = None
    description = None
    image_url = None
    thumb_url = None
    tags = None


class Gallery:
    url = None
    name = None
    images = None

    def __init__(self):
        self.images = []

    def add_image(self, image):
        self.images.append(image)


class ContextBuilder:
    context = None

    def __init__(self):
        self.context = {}
        self.update()

    def update(self):
        # Get galleries, only name and url
        im = Image()
        im.image_url = 'gallery/img/collage/7.jpg'
        im.thumb_url = 'gallery/img/collage/thumbs/7.jpg'
        im2 = Image()
        im2.image_url = 'gallery/img/collage/5.jpg'
        im2.thumb_url = 'gallery/img/collage/thumbs/5.jpg'

        gl = Gallery()
        gl.name = "Rooms"
        gl.url = "test1"
        gl.add_image(im)
        gl2 = Gallery()
        gl2.name = "Earth"
        gl2.url = "test2"
        gl2.add_image(im2)

        self.context['gallery_list'] = [gl, gl2]


class IndexContextBuilder(ContextBuilder):
    def update(self):
        super().update()


class GridContextBuilder(ContextBuilder):
    gallery_name = None

    def __init__(self, gallery_name):
        super().__init__()
        self.gallery_name = gallery_name
        self.update()

    def update(self):
        super().update()
        if self.gallery_name:
            self.context['gallery_name'] = self.gallery_name


def index(request):
    bldr = IndexContextBuilder()
    return render(request, 'index.html', bldr.context)


def grid(request, url_id):
    bldr = GridContextBuilder(url_id)
    return render(request, 'gallery.html', bldr.context)
