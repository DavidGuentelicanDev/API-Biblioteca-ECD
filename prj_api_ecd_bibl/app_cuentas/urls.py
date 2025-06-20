from django.urls import path
from . import views


urlpatterns = [
    path('status/', views.api_status, name='status_api'), #ruta inicial para verificar salud
    path('crear-usuario', views.CrearUsuarioAdminAPIView.as_view(), name='admin_crear_usuario') #ruta para crear usuario en app administradora
]