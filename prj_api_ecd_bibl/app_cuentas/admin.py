from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario


#* MODELO DE USUARIO PERSONALIZADO EN EL ADMIN
#20/06/25
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    #campos a mostrar en la lista del admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_superuser', 'is_active')

    #estructura de los campos en el formulario de detalle
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Información personal'), {'fields': ('first_name', 'last_name', 'email', 'rut', 'telefono', 'foto_perfil')}),
        (_('Permisos'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
        (_('Rol de usuario'), {'fields': ('rol',)}),
    )

    #estructura de los campos en el formulario de creacion
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'rut', 'telefono', 'rol', 'foto_perfil', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'username', 'first_name', 'last_name', 'rut')
    ordering = ('rol',)