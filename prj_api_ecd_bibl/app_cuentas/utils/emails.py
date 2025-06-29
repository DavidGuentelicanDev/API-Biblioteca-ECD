"""
EMAILS QUE SE ENVIAN AL CORREO REGISTRADO DEL USUARIO
"""


URL_BASE = 'http://127.0.0.1:8000/api/cuentas/'

#* EMAIL BIENVENIDA USUARIO NUEVO STAFF
#28/06/25

def enviar_email_bienvenida_usuario_nuevo_staff(usuario):
    subject = "Se ha creado un usuario para Admin ECD"
    ruta_activacion = f"{URL_BASE}v1/usuarios/nuevo/{usuario.username}/"
    message = (
        f"Hola {usuario.first_name},\n\n"
        f"Tu cuenta ha sido creada exitosamente. Para activar tu cuenta, haz click en el siguiente link: {ruta_activacion}\n\n"
        "Saludos,\n"
        "El equipo de la Biblioteca ECD"
    )
    from_email = 'no-reply@bibliotecaecd.cl'
    usuario.email_user(subject, message, from_email=from_email)

#######################################################################################################

#* EMAIL BIENVENIDA USUARIO NUEVO CLIENTE
#28/06/25

def enviar_email_bienvenida_usuario_nuevo_cliente(usuario):
    subject = 'Bienvenido/a a la Biblioteca ECD'
    ruta_activacion = f"{URL_BASE}v1/usuarios/nuevo/{usuario.username}/"
    message = (
        f"Hola {usuario.first_name},\n\n"
        f"Gracias por registrarte en nuestra plataforma. Tu cuenta ha sido creada exitosamente. Para activar tu cuenta, haz click en el siguiente link: {ruta_activacion}\n\n"
        "Saludos,\n"
        "El equipo de la Biblioteca ECD"
    )
    from_email = 'no-reply@bibliotecaecd.cl'
    usuario.email_user(subject, message, from_email=from_email)

#######################################################################################################

#* EMAIL DE RECUPERACIÓN DE CONTRASEÑA
#28/06/25

def enviar_email_recuperacion_password(usuario):
    subject = "Recuperación de contraseña - Biblioteca ECD"
    ruta_recuperacion = f"{URL_BASE}v1/usuarios/password/{usuario.username}/"
    message = (
        f"Hola {usuario.first_name},\n\n"
        f"Para recuperar tu contraseña, haz click en el siguiente link: {ruta_recuperacion}\n\n"
        "Si no solicitaste este cambio, ignora este correo.\n\n"
        "Saludos,\n"
        "El equipo de la Biblioteca ECD"
    )
    from_email = 'no-reply@bibliotecaecd.cl'
    usuario.email_user(subject, message, from_email=from_email)