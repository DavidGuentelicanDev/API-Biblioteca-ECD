from django.urls import path
from . import views


urlpatterns = [
    path('status/', views.api_status, name='status_api'), #ruta inicial para verificar salud
]