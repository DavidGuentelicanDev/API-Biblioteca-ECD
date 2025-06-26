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

################################################################################################

#* MODELO LIBRO
#25/06/25

class Libro(models.Model):
    #categorias de libro (las categorías pueden cambiar según la clasificación de cada Biblioteca)
    CATEGORIAS_LIBRO = (
        (1, 'Ficción'),
        (2, 'No ficción'),
    )

    #estados de libro (estos estados son genéricos para representar todo el proceso)
    ESTADOS_LIBRO = (
        (1, 'Ingresado'),     #recien ingresado a sistema, aun no disponible
        (2, 'Disponible'),    #disponible para reservas
        (3, 'Reservado'),     #reservado por un usuario
        (4, 'Prestado'),      #retirada la reserva, libro en manos del usuario
        (5, 'Devuelto'),      #libro devuelto por el usuario
        (6, 'Perdido'),       #libro perdido definitivamente
        (7, 'En reparación'), #libro dañado en proceso de reparacion
    )

    codigo       = models.PositiveSmallIntegerField(primary_key=True)
    titulo       = models.CharField(max_length=50)
    subtitulo    = models.CharField(max_length=50, blank=True, null=True)
    resena       = models.TextField(blank=True, null=True)
    categoria    = models.PositiveSmallIntegerField(choices=CATEGORIAS_LIBRO)
    editorial    = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    anio_edicion = models.CharField(max_length=4)
    portada      = models.ImageField(upload_to='images/book_covers', blank=True, null=True)
    estado       = models.PositiveSmallIntegerField(choices=ESTADOS_LIBRO, default=1) #por defecto: "Ingresado"

    class Meta:
        #restricciones
        constraints = [
            #check de categoria dentro de categorias de libro (se debe adaptar al diccionario)
            models.CheckConstraint(
                check=models.Q(categoria__in=[1, 2]),
                name='check_categoria_valida'
            ),
            #check de categoria dentro de estados de libro (se debe adaptar al diccionario)
            models.CheckConstraint(
                check=models.Q(estado__in=[1, 2, 3, 4, 5, 6, 7]),
                name='check_estado_valido'
            ),
        ]
        #indices
        indexes = [
            models.Index(fields=['categoria'], name='idx_libro_categoria'),
            models.Index(fields=['estado'], name='idx_libro_estado'),
            models.Index(fields=['titulo'], name='idx_libro_titulo'),
        ]

    def __str__(self):
        if self.subtitulo:
            return f"{self.titulo}. {self.subtitulo}"
        else:
            return str(self.titulo)