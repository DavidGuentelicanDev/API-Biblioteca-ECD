from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    #*GENERAL
    #salud
    path('status/', views.api_status, name='status_api'), #ruta inicial para verificar salud
    #patch
    path('usuario-inicial/<int:pk>/', views.ActivarUsuarioInicialAPIView.as_view(), name='usuario_inicial_activar'), #ruta para activar el usuario una vez creado

    #*JWT LOGIN Y LOGOUT
    path('admin/token/', views.CustomTokenObtainPairAdminView.as_view(), name='admin_token_obtain_pair'), #login admin
    path('web/token/', views.CustomTokenObtainPairWebView.as_view(), name='web_token_obtain_pair'), #login web
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'), #enviar refresh token
    path('logout/', views.LogoutAPIView.as_view(), name='blacklist_token'), #logout general

    #*ADMIN
    #post
    path('admin/crear-usuario/', views.CrearUsuarioAdminAPIView.as_view(), name='admin_crear_usuario'), #ruta para crear usuario en app administradora
    #get
    path('admin/usuarios/', views.UsuarioAdminListAPIView.as_view(), name='admin_usuarios_listar'), #ruta para obtener todos los usuarios admin
    path('admin/usuarios/<int:pk>/', views.UsuarioAdminRetrieveAPIView.as_view(), name='admin_usuarios_por_id'), #ruta para obtener usuario por id admin
    #patch
    path('admin/usuarios/<int:pk>/actualizar/', views.UsuarioAdminUpdateAPIView.as_view(), name='admin_usuario_actualizar'), #ruta para actualizar datos de usuario admin

    #*WEB
    #post
    path('web/registrar-usuario/', views.RegistrarUsuarioWebAPIView.as_view(), name='web_registrar_usuario'), #ruta para crear usuario en app web
    #get
    path('web/usuarios/<int:pk>/', views.UsuarioWebRetrieveAPIView.as_view(), name='web_usuarios_por_id'), #ruta para obtener usuario por id web
    #patch
    path('web/usuarios/<int:pk>/actualizar/', views.UsuarioWebUpdateAPIView.as_view(), name='web_usuario_actualizar'), #ruta para actualizar datos de usuario web
]