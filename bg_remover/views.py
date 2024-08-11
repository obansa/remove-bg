from io import BytesIO

from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from . import engine
from .models import BgRemover

from .serializer import RemoverSerialize, ImageUploadSerializer


class RemoverViewSet(viewsets.ModelViewSet):
    queryset = []
    serializer_class = RemoverSerialize


class ImageUploadViewSet(viewsets.GenericViewSet):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ImageUploadSerializer

    def create(self, request, *args, **kwargs):
        image = request.FILES.get('image')

        if not image:
            return Response({"error": "No image uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        input_image = Image.open(image)
        img_pil = engine.remove_bg_mult(input_image)

        img_io = BytesIO()
        img_pil.save(img_io, format='PNG')
        img_io.seek(0)

        # Return the processed image as a response
        response = HttpResponse(img_io, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="processed_image.png"'

        return response

