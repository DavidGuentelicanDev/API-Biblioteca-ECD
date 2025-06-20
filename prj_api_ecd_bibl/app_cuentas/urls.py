from django.urls import path
from . import views


urlpatterns = [
    path('status/', views.api_status, name='status_api'), #ruta inicial para verificar salud
    # path('crear-usuario', views.crear_usuario_app_admin, name='admin_crear_usuario') #ruta para crear usuario en app administradora
    path('crear-usuario', views.CrearUsuarioAdminAPIView.as_view(), name='admin_crear_usuario') #ruta para crear usuario en app administradora
]