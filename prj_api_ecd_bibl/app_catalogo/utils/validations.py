"""
VALIDACIONES PARA LA APP ADMIN
"""

from rest_framework import serializers


#VALIDACION AÑO EDICION
#26/06/25

def validate_anio_edicion(value):
    #valida que el campo año edición sólo contenga números
    if not value.isdigit():
        raise serializers.ValidationError("El año de edición debe contener solo números.")
    #valida que el campo año edición contenga máximo 4 dígitos
    if len(value) > 4:
        raise serializers.ValidationError("El año de edición debe tener máximo 4 dígitos.")
    return value