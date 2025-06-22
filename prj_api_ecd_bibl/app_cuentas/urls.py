from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('status/', views.api_status, name='status_api'), #ruta inicial para verificar salud
    #POST
    path('crear-usuario', views.CrearUsuarioAdminAPIView.as_view(), name='admin_crear_usuario'), #ruta para crear usuario en app administradora
    path('registrar-usuario', views.RegistrarUsuarioWebAPIView.as_view(), name='web_registrar_usuario'), #ruta para crear usuario en app web
    #JWT LOGIN
    path('token-admin/', views.CustomTokenObtainPairAdminView.as_view(), name='admin_token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
]