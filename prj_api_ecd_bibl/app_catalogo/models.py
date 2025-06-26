from django.db import models


#* MODELO EDITORIAL
#24/06/25

class Editorial(models.Model):
    id     = models.SmallAutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.nombre)

################################################################################################

#* MODELO AUTOR
#24/06/25
class Autor(models.Model):
    id         = models.SmallAutoField(primary_key=True)
    nombre     = models.CharField(max_length=50)
    pseudonimo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        #restricciones
        constraints = [
            #restriccion unique conjunta nombre-pseudonimo
            models.UniqueConstraint(fields=['nombre', 'pseudonimo'], name='un_autor_nombre_pseudonimo')
        ]
        #índices
        indexes = [
            models.Index(fields=['nombre'], name='idx_autor_nombre'),
            models.Index(fields=['pseudonimo'], name='idx_autor_pseudonimo'),
        ]

    def __str__(self):
        if self.pseudonimo:
            return str(self.pseudonimo)
        else:
            return str(self.nombre)