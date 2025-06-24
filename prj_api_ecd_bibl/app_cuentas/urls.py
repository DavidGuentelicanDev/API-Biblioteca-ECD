from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    #*GENERAL
    #salud
    path('status/', views.api_status, name='api_status'),
    #activar usuario nuevo
    path('usuarios/<int:pk>/', views.ActivarUsuarioInicialAPIView.as_view(), name='usuario_activar'),

    #*JWT LOGIN Y LOGOUT
    #login admin
    path('admin/token/', views.CustomTokenObtainPairAdminView.as_view(), name='admin_token_obtain_pair'),
    #login web
    path('web/token/', views.CustomTokenObtainPairWebView.as_view(), name='web_token_obtain_pair'),
    #refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    #logout
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),

    #*ADMIN
    #crear y listar usuarios
    path('admin/usuarios/', views.UsuarioAdminListCreateAPIView.as_view(), name='admin_usuarios_listar_crear'),
    #detalle de usuario por id
    path('admin/usuarios/<int:pk>/', views.UsuarioAdminRetrieveAPIView.as_view(), name='admin_usuarios_detalle'),
    #actualizar usuario
    path('admin/usuarios/<int:pk>/', views.UsuarioAdminUpdateAPIView.as_view(), name='admin_usuarios_actualizar'),

    #*WEB
    #registrar usuario
    path('web/usuarios/', views.RegistrarUsuarioWebAPIView.as_view(), name='web_usuarios_registrar'),
    #detalle de usuario por id
    path('web/usuarios/<int:pk>/', views.UsuarioWebRetrieveAPIView.as_view(), name='web_usuarios_detalle'),
    #actualizar usuario
    path('web/usuarios/<int:pk>/', views.UsuarioWebUpdateAPIView.as_view(), name='web_usuarios_actualizar'),
]