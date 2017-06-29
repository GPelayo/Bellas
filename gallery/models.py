from django.db import models


class BellObject(models.Model):
    pass


class BellGallery(BellObject):
    name = models.CharField(max_length=35)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


class BellImage(BellObject):
    name = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    image_location = models.CharField(max_length=300)
    thumbnail_location = models.CharField(max_length=300)
    parent_gallery = models.ForeignKey(BellGallery)
    source_id = models.CharField(max_length=35, unique=True)

    def __str__(self):
        return self.name
