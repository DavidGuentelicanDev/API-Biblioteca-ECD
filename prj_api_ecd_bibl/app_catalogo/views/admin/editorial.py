"""
RUTAS DE EDITORIAL
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Editorial
from ...serializers.admin.editorial import EditorialSerializer
from rest_framework.permissions import AllowAny


#* RUTA PARA LISTAR TODAS LAS EDITORIALES / CREAR EDITORIALES
#25/06/25

class EditorialListCreateAPIView(APIView):
    permission_classes = [AllowAny]

    #método para ruta get (listar)
    #25/06/25
    def get(self, request):
        editoriales = Editorial.objects.all()
        serializer = EditorialSerializer(editoriales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #método para ruta post (crear)
    #25/06/25
    def post(self, request):
        serializer = EditorialSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

############################################################################################

#* RUTA PARA FILTAR EDITORIAL POR ID / EDITAR EDITORIAL POR ID / ELIMINAR EDITORIAL POR ID
#25/06/25

class EditorialRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = [AllowAny]

    #método para filtrar editorial por id
    #25/06/25
    def get_editorial(self, pk):
        try:
            return Editorial.objects.get(pk=pk)
        except Editorial.DoesNotExist:
            return None

    #metodo para ruta get por id (listar)
    #25/06/25
    def get(self, request, pk):
        editorial = self.get_editorial(pk)

        if not editorial:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EditorialSerializer(editorial)
        return Response(serializer.data)

    #método para ruta put (actualizar)
    #25/06/25
    def put(self, request, pk):
        editorial = self.get_editorial(pk)

        if not editorial:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EditorialSerializer(editorial, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #método para ruta delete (eliminar)
    #25/06/25
    def delete(self, request, pk):
        editorial = self.get_editorial(pk)

        if not editorial:
            return Response({'detail': 'No encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        editorial.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)