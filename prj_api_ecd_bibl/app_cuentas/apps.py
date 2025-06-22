from django.apps import AppConfig


class AppCuentasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_cuentas'

    #metodo para incorporar las señales
    #22/06/25
    def ready(self):
        import app_cuentas.signals