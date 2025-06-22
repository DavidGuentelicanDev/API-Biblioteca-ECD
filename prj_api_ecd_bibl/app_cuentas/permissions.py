"""
PARA CREAR LOS PERMISOS SEGUN ROL DE USUARIO
"""

from rest_framework.permissions import BasePermission


#PERMISOS SOLO USUARIOS ADMIN (rol=1)
#21/06/25

class PermisoAdmin(BasePermission):
    def has_permission(self, request, view):
        return(
            request.user and
            request.user.is_authenticated and
            getattr(request.user, 'rol', None) == 1
        )


#PERMISOS SOLO USUARIOS ADMIN y BIBLIOTECARIO (rol=1 y 2)
#21/06/25

class PermisoBibliotecario(BasePermission):
    def has_permission(self, request, view):
        return(
            request.user and
            request.user.is_authenticated and
            getattr(request.user, 'rol', None) in [1, 2]
        )


#PERMISOS SOLO USUARIOS ADMIN, BIBLIOTECARIO y FUNCIONARIO (rol=1, 2 y 3)
#21/06/25

class PermisoFuncionario(BasePermission):
    def has_permission(self, request, view):
        return(
            request.user and
            request.user.is_authenticated and
            getattr(request.user, 'rol', None) in [1, 2, 3]
        )


#PERMISOS SOLO USUARIOS CLIENTE (rol=4)
#21/06/25

class PermisoCliente(BasePermission):
    def has_permission(self, request, view):
        return(
            request.user and
            request.user.is_authenticated and
            getattr(request.user, 'rol', None) == 4
        )