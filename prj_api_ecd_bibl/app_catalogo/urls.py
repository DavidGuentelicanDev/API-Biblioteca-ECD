from django.urls import path
from .views import status
from .views.admin.editorial import EditorialListCreateAPIView, EditorialRetrieveUpdateDeleteAPIView
from .views.admin.autor import AutorListCreateAPIView, AutorRetrieveUpdateDeleteAPIView
from .views.admin.libro import LibroListCreateAPIView


urlpatterns = [
    #* STATUS
    path('status/', status.api_status, name='api_status'),

    #* ADMIN
    #EDITORIAL
    #listar y crear editoriales
    path('admin/editoriales/', EditorialListCreateAPIView.as_view(), name='admin_editoriales_listar_crear'),
    #listar editorial por id | actualizar editorial | eliminar editorial
    path('admin/editoriales/<int:pk>/', EditorialRetrieveUpdateDeleteAPIView.as_view(), name='admin_editoriales_detalle_editar_eliminar'),
    #AUTOR
    #listar y crear autores
    path('admin/autores/', AutorListCreateAPIView.as_view(), name='admin_autores_listar_crear'),
    #listar autor por id | actualizar autor | eliminar autor
    path('admin/autores/<int:pk>/', AutorRetrieveUpdateDeleteAPIView.as_view(), name='admin_autores_detalle_editar_eliminar'),
    #LIBRO
    #listar y crear libros
    path('admin/libros/', LibroListCreateAPIView.as_view(), name='admin_libros_crear'),
]