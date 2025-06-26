from django.urls import path
from .views import status
from .views.admin.editorial import EditorialListCreateAPIView, EditorialRetrieveUpdateDeleteAPIView


urlpatterns = [
    #* STATUS
    path('status/', status.api_status, name='api_status'),

    #* ADMIN
    #EDITORIAL
    #listar y crear editoriales
    path('admin/editoriales/', EditorialListCreateAPIView.as_view(), name='admin_editoriales_list_create'),
    #listar editorial por id | actualizar editorial | eliminar editorial
    path('admin/editoriales/<int:pk>/', EditorialRetrieveUpdateDeleteAPIView.as_view(), name='admin_editoriales_detail_update_delete'),
]