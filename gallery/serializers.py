from rest_framework import serializers
from gallery.models import BellGallery, BellImage


class BellGallerySerializer(serializers.Serializer):
    gallery_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    slug = serializers.CharField(max_length=10)
    description = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)

    def create(self, validated_data):
        return BellGallery.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.slug = validated_data.get('slug')
        instance.description = validated_data.get('description')
        instance.save()
        return instance


class BellImageSerializer(serializers.Serializer):
    image_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    image_location = serializers.CharField(max_length=300)
    thumbnail_location = serializers.CharField(max_length=300)
    parent_gallery = serializers.StringRelatedField()
    source_id = serializers.CharField(max_length=35)

    def create(self, validated_data):
        return BellImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.width = validated_data.get('width')
        instance.height = validated_data.get('height')
        instance.image_location = validated_data.get('image_location')
        instance.thumbnail_location = validated_data.get('thumbnail_location')
        instance.parent_gallery = validated_data.get('parent_gallery')
        instance.source_id = validated_data.get('source_id')
        instance.save()
        return instance
