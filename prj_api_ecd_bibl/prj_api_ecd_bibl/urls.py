"""
URL configuration for prj_api_ecd_bibl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
#importaciones de swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API de Biblioteca Virtual ECD",
        default_version='v1',
        description="Documentación de la API",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="soporte@biblioteca.com"),
        # license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cuentas/', include('app_cuentas.urls')),
    path('api/catalogo/', include('app_catalogo.urls')),

    #swagger y redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # UI Swagger
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),           # UI Redoc
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),            # JSON puro
]

#! Sólo para desarrollo: para poder subir archivos (fotos) a carpeta media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#todo pendiente: configurar repositorio de archivos prod