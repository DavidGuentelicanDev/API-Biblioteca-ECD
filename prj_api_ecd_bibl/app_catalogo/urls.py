from django.urls import path
from .views import status
from .views.admin.editorial import EditorialListCreateAPIView, EditorialRetrieveUpdateDeleteAPIView
from .views.admin.autor import AutorListCreateAPIView, AutorRetrieveUpdateDeleteAPIView
from .views.admin.libro import LibroListCreateAPIView, LibroRetrieveUpdateDeleteAPIView
from .views.web.libro import LibroListAPIView, LibroRetrieveAPIView


urlpatterns = [
    #* STATUS
    path('v1/status/', status.api_status, name='api_status'),

    #* ADMIN
    #EDITORIAL
    #listar y crear editoriales
    path('v1/admin/editoriales/', EditorialListCreateAPIView.as_view(), name='admin_editoriales_listar_crear'),
    #listar editorial por id | actualizar editorial | eliminar editorial
    path('v1/admin/editoriales/<int:pk>/', EditorialRetrieveUpdateDeleteAPIView.as_view(), name='admin_editoriales_detalle_editar_eliminar'),
    #AUTOR
    #listar y crear autores
    path('v1/admin/autores/', AutorListCreateAPIView.as_view(), name='admin_autores_listar_crear'),
    #listar autor por id | actualizar autor | eliminar autor
    path('v1/admin/autores/<int:pk>/', AutorRetrieveUpdateDeleteAPIView.as_view(), name='admin_autores_detalle_editar_eliminar'),
    #LIBRO
    #listar y crear libros
    path('v1/admin/libros/', LibroListCreateAPIView.as_view(), name='admin_libros_listar_crear'),
    #listar libro por código | actualizar libro | eliminar libro
    path('v1/admin/libros/<str:codigo>/', LibroRetrieveUpdateDeleteAPIView.as_view(), name='admin_libros_detalle_editar_eliminar'),

    #* WEB
    #LIBRO
    #listar todos los libros
    path('v1/web/libros/', LibroListAPIView.as_view(), name='web_libros_listar'),
    #listar libro por código
    path('v1/web/libros/<str:codigo>/', LibroRetrieveAPIView.as_view(), name='web_libros_detalle'),
]