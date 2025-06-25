"""
SEÑALES POST SAVE, POST DELETE, PARA IMPORTAR COMO DECORADORES EN EL MODELO
"""

from django.db.models.signals import post_delete
from django.dispatch import receiver
from ..models import Usuario
import os


#SEÑAL POST_DELTE PARA BORRAR FOTO DE PERFIL AL BORRAR USUARIO
#22/06/25

@receiver(post_delete, sender=Usuario)
def eliminar_foto_perfil(sender, instance, **kwargs):
    if instance.foto_perfil and os.path.isfile(instance.foto_perfil.path):
        os.remove(instance.foto_perfil.path)