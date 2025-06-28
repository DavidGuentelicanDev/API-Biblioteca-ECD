from django.urls import path
from .views import general, auth, admin, web
from rest_framework_simplejwt.views import TokenRefreshView


#todo Actualizar contraseña debe ser resetear contraseña / actualizar contraseña se va a incoporar en actualizar usuario
#todo Juntar retrieve y update en una sola view
#todo revisar que pasa con los post

urlpatterns = [
    #*GENERAL
    #salud
    path('v1/status/', general.api_status, name='api_status'),
    #activar usuario nuevo
    path('v1/usuarios/nuevo/<str:username>/', general.ActivarUsuarioInicialAPIView.as_view(), name='usuario_activar'),
    #actualizar contraseña
    path('v1/usuarios/password/<int:pk>/', general.UsuarioActualizarPasswordAPIView.as_view(), name='password_actualizar'),

    #*JWT LOGIN Y LOGOUT
    #login admin
    path('v1/admin/token/', auth.CustomTokenObtainPairAdminView.as_view(), name='admin_token_obtain_pair'),
    #login web
    path('v1/web/token/', auth.CustomTokenObtainPairWebView.as_view(), name='web_token_obtain_pair'),
    #refresh
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    #logout
    path('v1/logout/', auth.LogoutAPIView.as_view(), name='logout'),

    #*ADMIN
    #crear y listar usuarios
    path('v1/admin/usuarios/', admin.UsuarioAdminListCreateAPIView.as_view(), name='admin_usuarios_listar_crear'),
    #detalle de usuario por username | actualizar usuario (con contraseña)
    path('v1/admin/usuarios/<str:username>/', admin.UsuarioAdminRetrieveUpdateAPIView.as_view(), name='admin_usuarios_detalle_actualizar'),

    #*WEB
    #registrar usuario
    path('v1/web/usuarios/', web.RegistrarUsuarioWebAPIView.as_view(), name='web_usuarios_registrar'),
    #detalle de usuario por id
    path('v1/web/usuarios/<int:pk>/', web.UsuarioWebRetrieveUpdateAPIView.as_view(), name='web_usuarios_detalle_actualizar'),
    #actualizar usuario
    # path('v1/web/usuarios/<int:pk>/', web.UsuarioWebUpdateAPIView.as_view(), name='web_usuarios_actualizar'),
]