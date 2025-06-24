from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('status/', views.api_status, name='status_api'), #ruta inicial para verificar salud
    #POST
    path('crear-usuario/', views.CrearUsuarioAdminAPIView.as_view(), name='admin_crear_usuario'), #ruta para crear usuario en app administradora
    path('registrar-usuario/', views.RegistrarUsuarioWebAPIView.as_view(), name='web_registrar_usuario'), #ruta para crear usuario en app web
    #JWT LOGIN Y LOGOUT
    path('token-admin/', views.CustomTokenObtainPairAdminView.as_view(), name='admin_token_obtain_pair'), #login admin
    path('token-web/', views.CustomTokenObtainPairWebView.as_view(), name='web_token_obtain_pair'), #login web
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('logout/', views.LogoutAPIView.as_view(), name='blacklist_token'), #logout general
    #GET
    path('usuarios/', views.UsuarioListAPIView.as_view(), name='usuarios_listar'), #ruta para obtener todos los usuarios
    path('usuarios/<int:pk>/', views.UsuarioRetrieveAPIView.as_view(), name='usuarios_filtro_por_id'), #ruta para obtener usuario por id
    #PUT
    #PATCH
    path('activar-usuario-inicial/<int:pk>/', views.ActivarUsuarioInicialAPIView.as_view(), name='usuario_inicial_activar'), #ruta para activar el usuario una vez creado
    path('usuarios/<int:pk>/admin-actualizar/', views.UsuarioAdminUpdateAPIView.as_view(), name='admin_usuario_actualizar'), #ruta para actualizar datos de usuario admin
    path('usuarios/<int:pk>/web-actualizar/', views.UsuarioWebUpdateAPIView.as_view(), name='web_usuario_actualizar'), #ruta para actualizar datos de usuario web
    #DELETE
]