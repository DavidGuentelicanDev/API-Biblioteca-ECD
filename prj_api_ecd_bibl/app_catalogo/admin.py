from django.contrib import admin
from .models import Editorial, Autor, Libro, AutorPorLibro


#IMPORTACIONES PARA EL ADMIN DE DJANGO
admin.site.register(Editorial)
admin.site.register(Autor)
admin.site.register(Libro)
admin.site.register(AutorPorLibro)