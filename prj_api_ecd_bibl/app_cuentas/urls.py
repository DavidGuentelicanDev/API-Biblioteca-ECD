from django.urls import path
from .views import general, auth, admin, web
from rest_framework_simplejwt.views import TokenRefreshView


#todo: modificar rutas para añadir versionado

urlpatterns = [
    #*GENERAL
    #salud
    path('status/', general.api_status, name='api_status'),
    #activar usuario nuevo
    path('usuarios/nuevo/<int:pk>/', general.ActivarUsuarioInicialAPIView.as_view(), name='usuario_activar'),
    #actualizar contraseña
    path('usuarios/password/<int:pk>/', general.UsuarioActualizarPasswordAPIView.as_view(), name='password_actualizar'),

    #*JWT LOGIN Y LOGOUT
    #login admin
    path('admin/token/', auth.CustomTokenObtainPairAdminView.as_view(), name='admin_token_obtain_pair'),
    #login web
    path('web/token/', auth.CustomTokenObtainPairWebView.as_view(), name='web_token_obtain_pair'),
    #refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    #logout
    path('logout/', auth.LogoutAPIView.as_view(), name='logout'),

    #*ADMIN
    #crear y listar usuarios
    path('admin/usuarios/', admin.UsuarioAdminListCreateAPIView.as_view(), name='admin_usuarios_listar_crear'),
    #detalle de usuario por id
    path('admin/usuarios/<int:pk>/', admin.UsuarioAdminRetrieveAPIView.as_view(), name='admin_usuarios_detalle'),
    #actualizar usuario
    path('admin/usuarios/<int:pk>/', admin.UsuarioAdminUpdateAPIView.as_view(), name='admin_usuarios_actualizar'),

    #*WEB
    #registrar usuario
    path('web/usuarios/', web.RegistrarUsuarioWebAPIView.as_view(), name='web_usuarios_registrar'),
    #detalle de usuario por id
    path('web/usuarios/<int:pk>/', web.UsuarioWebRetrieveAPIView.as_view(), name='web_usuarios_detalle'),
    #actualizar usuario
    path('web/usuarios/<int:pk>/', web.UsuarioWebUpdateAPIView.as_view(), name='web_usuarios_actualizar'),
]