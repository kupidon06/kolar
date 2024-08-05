# urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuration du schéma Swagger avec drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="API de Mon Projet",
        default_version='v1',
        description="Documentation de l'API pour mon projet Django",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@monprojet.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backends.urls')),
    path('api-auth/', include('rest_framework.urls')),

    # URL pour accéder à la documentation Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),

    # URL pour accéder à la documentation ReDoc
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),

    # URLs Djoser pour la gestion des utilisateurs
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
]
