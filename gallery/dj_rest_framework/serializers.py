from rest_framework import serializers


class IndexGallerySerializer(serializers.Serializer):
    name = serializers.CharField()
    slug = serializers.URLField()
    description = serializers.CharField()
    preview_image_url = serializers.URLField()


class PageImageSerializer(serializers.Serializer):
    name = serializers.CharField()
    image_url = serializers.URLField()
    thumb_url = serializers.URLField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()


class PageGallerySerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    images = PageImageSerializer(many=True)
