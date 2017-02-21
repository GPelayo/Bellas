from django.shortcuts import render


class Image:
    name = None
    description = None
    image_url = None
    thumb_url = None
    dimensions = None
    tags = None


class Gallery:
    url = None
    name = None
    images = None

    def __init__(self):
        self.images = []

    def add_image(self, image):
        self.images.append(image)

    def add_image_list(self, image_list):
        for imge in image_list:
            self.images.append(imge)


dummy_images = []

for i in range(1, 11):
    im = Image()
    im.image_url = 'gallery/img/original/{}.jpg'.format(i)
    im.thumb_url = 'gallery/img/thumbs/{}.jpg'.format(i)
    im.name = 'Image {}'.format(i)
    im.dimensions = "800x2000"
    dummy_images.append(im)


gl1 = Gallery()
gl1.name = "Rooms"
gl1.url = "Rooms"
gl1.add_image_list(dummy_images[1:3])
gl2 = Gallery()
gl2.name = "Earth"
gl2.url = "Earth"
gl2.add_image_list(dummy_images[3:12])

dummy_galleries = {gl1.name: gl1, gl2.name: gl2}


class ContextBuilder:
    context = None

    def __init__(self):
        self.context = {}
        self.update()

    def update(self):
        # Note: gallery_list is in every context because of the menu
        self.context['gallery_list'] = dummy_galleries.values()


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
            # replace with ORM call for retrieving gallery by name
            gl = dummy_galleries[self.gallery_name]
            self.context['gallery_name'] = gl.name
            self.context['image_list'] = gl.images


def index(request):
    bldr = IndexContextBuilder()
    return render(request, 'index.html', bldr.context)


def grid(request, url_id):
    bldr = GridContextBuilder(url_id)
    return render(request, 'gallery.html', bldr.context)
