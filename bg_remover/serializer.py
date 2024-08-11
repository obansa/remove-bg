import os

from PIL import Image
from io import BytesIO

from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import BgRemover
from . import engine
from django.conf import settings


class RemoverSerialize(serializers.ModelSerializer):
    img = serializers.ImageField()
    result = serializers.ImageField(read_only=True)

    class Meta:
        model = BgRemover
        fields = ['img', 'result']

    def create(self, validated_data):
        import_data = BgRemover.objects.create(img=validated_data['img'])

        input_image = Image.open(import_data.img)
        img_pil = engine.remove_bg_mult(input_image)
        image_io = BytesIO()

        # img_pil.save(output_image)
        img_pil.save(image_io, format='PNG')
        image_io.seek(0)

        output_name, _ = os.path.splitext(os.path.basename(import_data.img.name))
        import_data.result.save(f"{output_name}.png", ContentFile(image_io.read()), save=False)

        import_data.save()

        # Return user and token in the response
        return {
            'img': import_data.img,
            'result': import_data.result
        }


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, value):
        return value