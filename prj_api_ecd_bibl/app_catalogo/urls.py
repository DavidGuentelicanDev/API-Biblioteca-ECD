from django.urls import path
from .views.admin.editorial import EditorialListCreateAPIView, EditorialRetrieveUpdateDeleteAPIView


urlpatterns = [
    #* ADMIN
    #EDITORIAL
    #listar y crear editoriales
    path('admin/editoriales/', EditorialListCreateAPIView.as_view(), name='admin_editoriales_list_create'),
    #listar editorial por id | actualizar editorial | eliminar editorial
    path('admin/editoriales/<int:pk>/', EditorialRetrieveUpdateDeleteAPIView.as_view(), name='admin_editoriales_detail_update_delete'),
]