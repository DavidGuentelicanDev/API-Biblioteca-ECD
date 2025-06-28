"""
RUTAS DE AUTOR
"""

from rest_framework.response import Response
from rest_framework import generics, status
from ...models import Autor
from ...serializers.admin.autor import AutorSerializer
from app_cuentas.utils.permissions import PermisoBibliotecario, PermisoFuncionario
from ...utils.paginations import AdminPagination


#* RUTA PARA LISTAR TODOS LOS AUTORES / CREAR AUTORES
#25/06/25

class AutorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Autor.objects.all().order_by('nombre')
    serializer_class = AutorSerializer
    pagination_class = AdminPagination

    #método para identificar permisos según método HTTP
    #28/06/25
    def get_permissions(self):
        #si es GET, permiso de funcionario
        if self.request.method == 'GET':
            return [PermisoFuncionario()]
        #si es POST, permiso de bibliotecario
        return [PermisoBibliotecario()]

    #método para ruta post (create)
    #25/06/25
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            autor = serializer.save()
            return Response({
                "status": "success",
                "message": f"Autor {str(autor)} creado exitosamente.",
                "autor": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "message": "Error al crear el autor.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

############################################################################################

#* RUTA PARA FILTAR EDITORIAL POR ID / EDITAR EDITORIAL POR ID / ELIMINAR EDITORIAL POR ID
#25/06/25

class AutorRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer

    #método para identificar permisos según método HTTP
    #28/06/25
    def get_permissions(self):
        #si es GET, permiso de funcionario
        if self.request.method == 'GET':
            return [PermisoFuncionario()]
        #si es POST, permiso de bibliotecario
        return [PermisoBibliotecario()]

    #método para ruta put (update)
    #26/06/25
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            autor = serializer.save()
            return Response({
                "status": "success",
                "message": f"Autor {str(autor)} actualizada exitosamente.",
                "autor": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "Error al actualizar el autor.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    #método para ruta delete
    #26/06/25
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            self.perform_destroy(instance)
            return Response({
                "status": "success",
                "message": f"Autor {str(instance)} eliminado exitosamente."
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error al borrar el autor.",
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)