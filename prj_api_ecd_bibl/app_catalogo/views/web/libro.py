"""
RUTAS DE LIBRO WEB
"""

from rest_framework import generics, status
from rest_framework.response import Response
from ...models import Libro
from ...serializers.web.libro import LibroWebListSerializer
from rest_framework.permissions import AllowAny


class LibroListAPIView(generics.ListAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroWebListSerializer
    permission_classes = [AllowAny]