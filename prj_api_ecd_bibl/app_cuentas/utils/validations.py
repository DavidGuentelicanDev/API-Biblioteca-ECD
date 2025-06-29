"""
VALIDACIONES Y FORMATOS DE CAMPOS
"""

import re
from rest_framework import serializers


#VALIDACION FORMATO TELEFONO
#24/06/25

def validate_telefono(value):
    if value == "":
        return None
    patron = r'^\+569\d{8}$'
    if not re.match(patron, value):
        raise serializers.ValidationError("El teléfono debe tener formato +569XXXXXXXX, donde X son números.")
    return value

#######################################################################################

#VALIDACION FORMATO RUT
#24/06/25

def validate_rut(value):
    patron = r'^\d{7,8}-[\dkK]$'
    if not re.match(patron, value):
        raise serializers.ValidationError("El RUT debe tener el formato XXXXXXXX-K, donde X son números y K es un número o la letra k/K.")
    return value