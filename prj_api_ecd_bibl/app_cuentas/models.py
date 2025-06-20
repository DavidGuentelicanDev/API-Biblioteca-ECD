from django.db import models
from django.contrib.auth.models import AbstractUser


#* MODELO DE USUARIO PERSONALIZADO
#20/06/25

class Usuario(AbstractUser):
    #roles de usuario definido
    ROLES_USUARIO = (
        (1, 'Administrador'),
        (2, 'Bibliotecario'),
        (3, 'Funcionario'),
        (4, 'Cliente'),
    )

    #campos personalizados
    rut         = models.CharField(max_length=10, unique=True)
    telefono    = models.CharField(max_length=12, unique=True, blank=True, null=True)
    rol         = models.PositiveSmallIntegerField(choices=ROLES_USUARIO)
    foto_perfil = models.ImageField(upload_to='images/profile', blank=True, null=True)

    #redefinir campos heredados
    first_name = models.CharField(max_length=150, blank=False)
    last_name  = models.CharField(max_length=150, blank=False)
    email      = models.EmailField(blank=False, unique=True)

    class Meta:
        #indices
        indexes = [
            models.Index(fields=['rut'], name='idx_usuario_rut'),
            models.Index(fields=['telefono'], name='idx_usuario_telefono'),
            models.Index(fields=['rol'], name='idx_usuario_rol'),
            models.Index(fields=['email'], name='idx_usuario_email'),
            models.Index(fields=['is_staff'], name='idx_usuario_staff'),
        ]
        #restricciones
        constraints = [
            #check de rol dentro de roles de usuario, se debe adaptar al diccionario
            models.CheckConstraint(
                check=models.Q(rol__in=[1, 2, 3, 4]),
                name='check_rol_valido'
            )
        ]

    def __str__(self):
        return f"{self.get_full_name().strip()} - {self.get_rol_display()}"