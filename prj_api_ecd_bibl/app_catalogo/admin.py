from django.contrib import admin
from .models import Editorial, Autor


#IMPORTACIONES PARA EL ADMIN DE DJANGO
admin.site.register(Editorial)
admin.site.register(Autor)